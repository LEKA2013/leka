# Inventário de dados — MERGE + ERA5 (Amazônia)

Documento vivo da **Fase 0**. Registra o que a equipe já definiu e o que ainda precisa ser preenchido **na máquina com acesso à rede CENSIPAM**.

> **Restrição:** o agente em nuvem Cursor **não** acessa `\\files-be\NCEP\era5`. Nenhum catálogo abaixo foi obtido por varredura remota. Padrões de nome de arquivo e listagens reais devem ser anotados por quem estiver na rede institucional.

---

## 1. Caminhos institucionais

| Fonte | Path padrão / status | Override (env) |
|-------|----------------------|----------------|
| ERA5 / dados climáticos da equipe | `\\files-be\NCEP\era5` (Windows UNC) | `CENSIPAM_ERA5_ROOT` |
| MERGE (precipitação) | `S:\Leticia\dados_INPE\MERGE_NC` (informado pela usuária; dados diários) | `CENSIPAM_MERGE_ROOT` |
| Máscara Amazônia Legal | **TBD** — shapefile/GeoJSON a fornecer (sem geometria inventada no repo) | `CENSIPAM_AMAZONIA_LEGAL_MASK` |

Em Linux/WSL ou cópia autorizada, remapeie via variáveis de ambiente (ver `.env.example` e `configs/paths.example.yaml`).

---

## 2. Domínios

| Domínio | Prioridade | Geometria |
|---------|------------|-----------|
| **Amazônia Legal** | Primeiro (Track 1) | Máscara oficial / a usada no CENSIPAM — **a obter**; colocar em `data/masks/` |
| Bacia amazônica | Depois (fases posteriores) | Ainda não | 

Bounding box opcional pode ser anotado abaixo só para exploração grosseira — **não** substitui a máscara.

- BBox Amazônia Legal (opcional): _a preencher se útil_ — lon_min / lon_max / lat_min / lat_max: ________

---

## 3. Precipitação — MERGE

| Item | Valor |
|------|--------|
| Papel | Única fonte de precipitação neste ciclo (não usar precip ERA5) |
| Frequência | **Diária** (confirmado pela usuária) |
| Climatologia de referência | **2001–2020** |
| String de produto / versão | **Em aberto** — anotar quando confirmada |
| Path | `S:\Leticia\dados_INPE\MERGE_NC` (`CENSIPAM_MERGE_ROOT`) |
| Formato sugerido pelo nome da pasta | NetCDF (`.nc`) — confirmar nos arquivos |

### Checklist MERGE (preencher na rede CENSIPAM)

- [x] Path completo confirmado — `S:\Leticia\dados_INPE\MERGE_NC`
- [x] Frequência — diária
- [ ] Nome/versão do produto (string)
- [ ] Extensão / formato confirmado nos arquivos (pasta sugere NetCDF)
- [ ] Padrão de nome de arquivo (ex.: prefixo, data `YYYYMMDD`, grade)
- [ ] Resolução espacial e grade
- [ ] Período disponível no compartilhamento
- [ ] Arquivo(s) da climatologia 2001–2020 (ou se é calculada no pipeline)
- [ ] Exemplo de path de **um** arquivo de um dia (copie o nome completo): ________

---

## 4. ERA5 — variáveis diárias em uso

| Variável (lógica) | Status | Notas |
|-------------------|--------|-------|
| TSM (SST) | Em uso | Temperatura da superfície do mar |
| OMEGA | Em uso | Velocidade vertical |
| U | Em uso; **download em andamento** | Componente zonal do vento |
| V | Em uso; **download em andamento** | Componente meridional do vento |
| Temperatura média do ar | Em uso | |
| Umidade relativa | Em uso | |

Frequência declarada pela equipe: **diária**.

### Checklist ERA5 sob `\\files-be\NCEP\era5` (preencher na rede)

- [ ] Estrutura de pastas (por variável? por ano?)
- [ ] Formato (NetCDF / GRIB / outro) e engine sugerida (`netcdf4` / `h5netcdf` / `cfgrib`)
- [ ] Padrão de nome — TSM: ________
- [ ] Padrão de nome — OMEGA: ________
- [ ] Padrão de nome — U: ________
- [ ] Padrão de nome — V: ________
- [ ] Padrão de nome — temp. média do ar: ________
- [ ] Padrão de nome — umidade relativa: ________
- [ ] Resolução espacial / níveis (se aplicável)
- [ ] Período disponível por variável
- [ ] Nomes das variáveis *dentro* dos arquivos (CF / shortName): ________

Não inventar entradas acima. Deixar em branco até inspeção local.

---

## 5. Climatologia de chuva

- Período de referência: **2001–2020** (confirmado pela usuária; “já na versão nova”).
- Produto: MERGE.
- Cálculo no pipeline (Fase 1) vs. arquivo pré-existente: _a confirmar no inventário local_.

---

## 6. O que este inventário **não** afirma

- Que o UNC foi listado ou montado por este scaffold.
- Catálogo completo de arquivos ou tamanhos.
- Políticas institucionais de compartilhamento (ainda não documentadas no projeto).

---

## 7. Próximos passos (máquina CENSIPAM)

1. Exportar `CENSIPAM_ERA5_ROOT` e `CENSIPAM_MERGE_ROOT=S:\Leticia\dados_INPE\MERGE_NC`.
2. Copiar/apontar a máscara Amazônia Legal e definir `CENSIPAM_AMAZONIA_LEGAL_MASK`.
3. Abrir a pasta MERGE no Explorer, copiar o nome de **um** arquivo `.nc` de um dia e colar no checklist acima.
4. Rodar `python scripts/check_paths.py` e o notebook `notebooks/00_exploracao_dominio.ipynb`.
