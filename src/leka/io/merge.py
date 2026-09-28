"""Stubs de leitura MERGE (precipitação).

A string de produto/versão MERGE e o path institucional ainda estão em aberto.
Não inventar nomes de arquivo nem catálogo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from leka.config import DataPaths, load_paths, path_exists


class DataUnavailableError(FileNotFoundError):
    """Dados MERGE não encontrados ou path não configurado."""


def list_merge_candidates(
    paths: DataPaths | None = None,
    patterns: Iterable[str] | None = None,
) -> list[Path]:
    """Lista arquivos MERGE sob a raiz configurada.

    Sem ``CENSIPAM_MERGE_ROOT`` / config, falha de forma controlada.
    Sem ``patterns``, não varre a árvore com padrões inventados.
    """
    paths = paths or load_paths()
    root = paths.merge_root
    if root is None:
        raise DataUnavailableError(
            "Path MERGE não configurado. Defina CENSIPAM_MERGE_ROOT ou "
            "preencha merge.root em configs/paths.yaml (ainda TBD)."
        )
    if not path_exists(root):
        raise DataUnavailableError(
            f"Raiz MERGE inacessível: {root}. Verifique o path na rede CENSIPAM."
        )
    if not patterns:
        return []
    found: list[Path] = []
    for pattern in patterns:
        found.extend(sorted(root.glob(pattern)))
    return found


def open_merge_sample(
    paths: DataPaths | None = None,
    *,
    relative_path: str | None = None,
    patterns: Iterable[str] | None = None,
):
    """Abre um arquivo MERGE de amostra com xarray (quando o path existir)."""
    paths = paths or load_paths()
    root = paths.merge_root
    if root is None:
        raise DataUnavailableError(
            "Path MERGE não configurado (CENSIPAM_MERGE_ROOT / configs)."
        )
    if not path_exists(root):
        raise DataUnavailableError(f"Raiz MERGE inacessível: {root}")

    if relative_path:
        target = root / relative_path
        if not path_exists(target):
            raise DataUnavailableError(f"Arquivo MERGE não encontrado: {target}")
    elif patterns:
        candidates = list_merge_candidates(paths, patterns=patterns)
        if not candidates:
            raise DataUnavailableError(
                f"Nenhum arquivo MERGE correspondente a {list(patterns)} em {root}"
            )
        target = candidates[0]
    else:
        raise DataUnavailableError(
            "Informe relative_path ou patterns após documentar o produto MERGE "
            "em docs/inventario-dados.md."
        )

    import xarray as xr

    return xr.open_dataset(target)
