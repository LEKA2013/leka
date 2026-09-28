"""Máscara da Amazônia Legal.

A geometria **deve ser fornecida** pela equipe (shapefile/GeoJSON oficial ou o
já usado no CENSIPAM). Este módulo **não** inventa polígonos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from leka.config import DataPaths, load_paths, path_exists


class MaskUnavailableError(FileNotFoundError):
    """Máscara da Amazônia Legal ausente ou inacessível."""


def load_amazonia_legal_mask(paths: DataPaths | None = None):
    """Carrega a geometria da Amazônia Legal via geopandas.

    Raises
    ------
    MaskUnavailableError
        Se o path não estiver configurado ou o arquivo não existir.
    """
    paths = paths or load_paths()
    mask_path = paths.amazonia_legal_mask
    if mask_path is None:
        raise MaskUnavailableError(
            "Máscara da Amazônia Legal não configurada. "
            "Coloque o shapefile/GeoJSON em data/masks/ e defina "
            "CENSIPAM_AMAZONIA_LEGAL_MASK (ou masks.amazonia_legal no YAML). "
            "Não há geometria inventada neste repositório."
        )
    if not path_exists(mask_path):
        raise MaskUnavailableError(
            f"Arquivo de máscara não encontrado: {mask_path}. "
            "Verifique o path na máquina CENSIPAM."
        )

    import geopandas as gpd

    return gpd.read_file(mask_path)


def mask_amazonia_legal(ds: Any, paths: DataPaths | None = None):
    """Aplica a máscara da Amazônia Legal a um Dataset/DataArray xarray.

    Stub Fase 0: carrega a geometria e documenta o contrato. A implementação
    completa (rasterização / rioxarray / regionmask) entra nas fases seguintes
    quando a máscara oficial estiver disponível.
    """
    gdf = load_amazonia_legal_mask(paths)
    raise NotImplementedError(
        "mask_amazonia_legal: geometria carregada "
        f"({len(gdf)} feição(ões)), mas o recorte raster ainda não foi "
        "implementado (Fase 1). Forneça a máscara e avance o pipeline de "
        "climatologia/anomalias na máquina com dados."
    )
