# Letícia Cardoso — clima Amazônia (CENSIPAM)

Repositório de análise climática da equipe de clima do **CENSIPAM**, com foco na **Amazônia Legal** (depois bacia amazônica). Pipeline compartilhado: **MERGE** (precipitação) + **ERA5** (reanálise), em **Python**.

**Agora = Track 1 / Fase 0:** fundação do repositório, inventário e stubs de leitura. Ainda **não** há composites, dashboard nem análises completas neste scaffold.

---

## Layout

```
leka/
├── configs/           # Exemplo de paths (YAML); copie para paths.yaml se quiser
├── data/
│   ├── raw/           # Dados brutos locais (gitignored)
│   ├── processed/     # Produtos processados (gitignored)
│   └── masks/         # Máscara Amazônia Legal fornecida pela equipe
├── docs/
│   └── inventario-dados.md
├── notebooks/
│   └── 00_exploracao_dominio.ipynb
├── scripts/
│   └── check_paths.py
├── src/leka/          # Pacote Python (config, io, domínio)
├── requirements.txt
└── README.md
```

---

## Ambiente

Python ≥ 3.10 recomendado.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export PYTHONPATH=src       # ou: pip install -e .  se usar pyproject
```

Dependências principais: `xarray`, `netCDF4` / `h5netcdf`, `cfgrib`, `numpy`, `pandas`, `matplotlib`, `cartopy`, `geopandas`, `jupyter`.

> **Nota:** `cfgrib` / `eccodes` podem exigir bibliotecas do sistema no Linux. No Windows institucional, use o ambiente já validado pela equipe se a instalação local falhar.

---

## Caminhos de dados

| Recurso | Padrão | Variável de ambiente |
|---------|--------|----------------------|
| ERA5 / clima institucional | `\\files-be\NCEP\era5` | `CENSIPAM_ERA5_ROOT` |
| MERGE (precip, diário) | `S:\Leticia\dados_INPE\MERGE_NC` | `CENSIPAM_MERGE_ROOT` |
| Máscara Amazônia Legal | a fornecer em `data/masks/` | `CENSIPAM_AMAZONIA_LEGAL_MASK` |

O cloud agent **não** lê esses paths de rede. Em máquina CENSIPAM (Windows):

```powershell
$env:CENSIPAM_ERA5_ROOT = "\\files-be\NCEP\era5"
$env:CENSIPAM_MERGE_ROOT = "S:\Leticia\dados_INPE\MERGE_NC"
# $env:CENSIPAM_AMAZONIA_LEGAL_MASK = "C:\caminho\para\mascara.shp"
```

Linux / cópia autorizada: aponte `CENSIPAM_ERA5_ROOT` para o mount ou diretório local. Veja `.env.example` e `configs/paths.example.yaml`.

Verificação rápida:

```bash
PYTHONPATH=src python scripts/check_paths.py
```

---

## Fase 0 vs. tracks seguintes

| Fase / Track | Conteúdo | Neste repo agora? |
|--------------|----------|-------------------|
| **Fase 0 (Track 1)** | Layout, deps, config, inventário, stubs, notebook que falha com graça sem dados | **Sim** |
| Fase 1 (Track 1) | Climatologia MERGE 2001–2020, anomalias, leitura real ERA5 no domínio | Não |
| Fase 1b (Track 1) | Composites ENSO + dipolo Atlântico × precip Amazônia Legal | Não |
| Track 2 | Dashboard MVP interativo (Streamlit, ponto de grade MERGE) | Não |
| Track 3 | Extremos (seca / chuva intensa) | Não |

Documentação de planejamento de longo prazo fica na Agent Store do projeto Cursor; aqui no git fica o código e o inventário operacional.

---

## Máscara Amazônia Legal

**Não há geometria inventada.** Coloque o shapefile/GeoJSON oficial (ou o já usado no CENSIPAM) em `data/masks/` e configure o path. O stub `leka.domain.mask_amazonia_legal` carrega a máscara quando existir; o recorte raster completo entra na Fase 1.

---

## Notebook de exploração

`notebooks/00_exploracao_dominio.ipynb` — verifica paths e tenta abrir amostra só se você informar padrões/arquivos conhecidos. Sem dados, termina com mensagem clara (não quebra o ambiente).

---

## Credibilidade

- Sem resultados fictícios nem arquivos de dados falsos.
- Inventário: checklist para preencher na rede; padrões de nome **não** foram inventados.
- U/V: marcados como download em andamento no inventário.

---

## Autoria

Letícia Cardoso — CENSIPAM / pesquisa climática Amazônia.
