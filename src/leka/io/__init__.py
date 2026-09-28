"""Leitores de dados (stubs Fase 0)."""

from .era5 import list_era5_candidates, open_era5_sample
from .merge import list_merge_candidates, open_merge_sample

__all__ = [
    "list_era5_candidates",
    "open_era5_sample",
    "list_merge_candidates",
    "open_merge_sample",
]
