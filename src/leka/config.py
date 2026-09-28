"""Carregamento de caminhos de dados (ERA5, MERGE, máscaras).

Precedência: variável de ambiente > configs/paths.yaml > padrão UNC.
O cloud agent Cursor não acessa ``\\\\files-be\\NCEP\\era5``; use override
local (Linux/WSL) via ``CENSIPAM_ERA5_ROOT`` quando houver cópia autorizada.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# Padrão institucional informado pela equipe (Windows UNC).
DEFAULT_ERA5_ROOT = r"\\files-be\NCEP\era5"

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_CANDIDATES = (
    REPO_ROOT / "configs" / "paths.yaml",
    REPO_ROOT / "configs" / "paths.example.yaml",
)


@dataclass(frozen=True)
class DataPaths:
    """Raízes de dados resolvidas para a sessão atual."""

    era5_root: Path | None
    merge_root: Path | None
    amazonia_legal_mask: Path | None
    precip_clim_start: int = 2001
    precip_clim_end: int = 2020

    def summary(self) -> dict[str, Any]:
        return {
            "era5_root": _path_str(self.era5_root),
            "merge_root": _path_str(self.merge_root),
            "amazonia_legal_mask": _path_str(self.amazonia_legal_mask),
            "precip_clim_period": f"{self.precip_clim_start}-{self.precip_clim_end}",
        }


def _path_str(path: Path | None) -> str | None:
    return None if path is None else str(path)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config inválida (esperado mapping): {path}")
    return data


def _resolve_config_file(config_path: Path | None = None) -> Path | None:
    if config_path is not None:
        return config_path if config_path.is_file() else None
    for candidate in DEFAULT_CONFIG_CANDIDATES:
        if candidate.is_file():
            return candidate
    return None


def _as_path(value: Any) -> Path | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"null", "none", "tbd"}:
        return None
    return Path(text)


def load_paths(config_path: Path | None = None) -> DataPaths:
    """Resolve caminhos de dados a partir de env + YAML.

    Variáveis de ambiente:
      - ``CENSIPAM_ERA5_ROOT``
      - ``CENSIPAM_MERGE_ROOT``
      - ``CENSIPAM_AMAZONIA_LEGAL_MASK``
    """
    cfg_file = _resolve_config_file(config_path)
    cfg = _load_yaml(cfg_file) if cfg_file else {}

    era5_cfg = cfg.get("era5") or {}
    merge_cfg = cfg.get("merge") or {}
    masks_cfg = cfg.get("masks") or {}
    clim_cfg = (cfg.get("climatology") or {}).get("precip_reference_period") or {}

    era5_env = era5_cfg.get("env_var", "CENSIPAM_ERA5_ROOT")
    merge_env = merge_cfg.get("env_var", "CENSIPAM_MERGE_ROOT")
    mask_env = masks_cfg.get("env_var", "CENSIPAM_AMAZONIA_LEGAL_MASK")

    era5_root = _as_path(os.environ.get(era5_env)) or _as_path(
        era5_cfg.get("root", DEFAULT_ERA5_ROOT)
    )
    if era5_root is None:
        era5_root = Path(DEFAULT_ERA5_ROOT)

    merge_root = _as_path(os.environ.get(merge_env)) or _as_path(merge_cfg.get("root"))
    mask_path = _as_path(os.environ.get(mask_env)) or _as_path(
        masks_cfg.get("amazonia_legal")
    )

    return DataPaths(
        era5_root=era5_root,
        merge_root=merge_root,
        amazonia_legal_mask=mask_path,
        precip_clim_start=int(clim_cfg.get("start", 2001)),
        precip_clim_end=int(clim_cfg.get("end", 2020)),
    )


def path_exists(path: Path | None) -> bool:
    """Verifica existência sem lançar; UNC inacessível retorna False."""
    if path is None:
        return False
    try:
        return path.exists()
    except OSError:
        return False
