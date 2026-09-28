#!/usr/bin/env python3
"""Verifica configuração de caminhos (sem exigir dados acessíveis).

Uso (na raiz do repo, com PYTHONPATH=src ou pip install -e .)::

    python scripts/check_paths.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from leka.config import load_paths, path_exists  # noqa: E402


def main() -> int:
    paths = load_paths()
    print("Configuração resolvida:")
    for key, value in paths.summary().items():
        print(f"  {key}: {value}")

    print("\nAcessibilidade nesta máquina:")
    checks = {
        "ERA5": paths.era5_root,
        "MERGE": paths.merge_root,
        "Máscara Amazônia Legal": paths.amazonia_legal_mask,
    }
    for label, path in checks.items():
        if path is None:
            status = "não configurado"
        elif path_exists(path):
            status = "acessível"
        else:
            status = "inacessível (esperado fora da rede CENSIPAM / sem cópia local)"
        print(f"  {label}: {status}")

    print(
        "\nNota: este script não lista o catálogo UNC nem inventa arquivos. "
        "Preencha docs/inventario-dados.md na rede institucional."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
