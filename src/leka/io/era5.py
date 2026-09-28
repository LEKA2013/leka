"""Stubs de leitura ERA5.

Não inventa nomes de arquivo. Em ambiente sem acesso ao UNC, as funções
falham de forma controlada e orientam a configurar ``CENSIPAM_ERA5_ROOT``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from leka.config import DataPaths, load_paths, path_exists

# Variáveis diárias em uso pela equipe (nomes lógicos — mapeamento de arquivo a preencher).
ERA5_VARIABLES = (
    "tsm",  # SST / temperatura da superfície do mar
    "omega",
    "u",
    "v",
    "temp_media_ar",
    "ur",  # umidade relativa
)


class DataUnavailableError(FileNotFoundError):
    """Dados não encontrados ou path inacessível nesta máquina."""


def list_era5_candidates(
    paths: DataPaths | None = None,
    patterns: Iterable[str] | None = None,
) -> list[Path]:
    """Lista arquivos sob a raiz ERA5 que batem com *patterns*.

    Se ``patterns`` for ``None``, retorna lista vazia e não faz varredura
    inventada — o inventário de padrões de nome deve ser preenchido na rede
    CENSIPAM (ver ``docs/inventario-dados.md``).
    """
    paths = paths or load_paths()
    root = paths.era5_root
    if not path_exists(root):
        raise DataUnavailableError(
            f"Raiz ERA5 inacessível: {root!s}. "
            "Defina CENSIPAM_ERA5_ROOT na máquina com acesso à rede institucional "
            "ou a uma cópia autorizada."
        )
    if not patterns:
        return []
    found: list[Path] = []
    assert root is not None
    for pattern in patterns:
        found.extend(sorted(root.glob(pattern)))
    return found


def open_era5_sample(
    paths: DataPaths | None = None,
    *,
    relative_path: str | None = None,
    patterns: Iterable[str] | None = None,
):
    """Abre um arquivo ERA5 de amostra com xarray.

    Informe ``relative_path`` (relativo à raiz ERA5) ou ``patterns`` de glob
    conhecidos após o inventário na rede CENSIPAM. Sem isso, levanta erro
    explícito — não escolhe arquivo arbitrário.
    """
    paths = paths or load_paths()
    root = paths.era5_root
    if not path_exists(root):
        raise DataUnavailableError(
            f"Raiz ERA5 inacessível: {root!s}. "
            "Configure CENSIPAM_ERA5_ROOT e verifique o inventário."
        )
    assert root is not None

    if relative_path:
        target = root / relative_path
        if not path_exists(target):
            raise DataUnavailableError(f"Arquivo ERA5 não encontrado: {target}")
    elif patterns:
        candidates = list_era5_candidates(paths, patterns=patterns)
        if not candidates:
            raise DataUnavailableError(
                f"Nenhum arquivo ERA5 correspondente a {list(patterns)} em {root}"
            )
        target = candidates[0]
    else:
        raise DataUnavailableError(
            "Informe relative_path ou patterns após preencher o checklist "
            "em docs/inventario-dados.md (padrões de nome ainda não documentados)."
        )

    import xarray as xr

    # engine=None deixa o xarray escolher (netcdf4 / h5netcdf / cfgrib conforme extensão)
    return xr.open_dataset(target)
