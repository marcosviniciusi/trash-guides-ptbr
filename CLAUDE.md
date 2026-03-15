# CLAUDE.md - Contexto do Projeto TRaSH Guides PT-BR

## Visao Geral
Repositorio de Custom Formats em Portugues Brasileiro para Radarr e Sonarr, com automacao via Configarr (Docker/Kubernetes).

## Estrutura de Arquivos Importantes

### Custom Formats (custom-formats/)
Arquivos JSON locais referenciados nos configs via `trash_ids`:

**PT-BR Especificos:**
- `custom-brazilian-group-tier-dual-audio.json` - Grupos PT-BR com dual audio
- `custom-brazilian-dual-language.json` - Deteccao de dual language
- `custom-brazilian-group-tier-subtitles.json` - Grupos PT-BR com legendas
- `custom-brazilian-subtitles.json` - Deteccao de legendas PT-BR
- `custom-brazilian-group-tier-dubbed.json` - Grupos PT-BR com dublagem
- `custom-brazilian-dubbed.json` - Deteccao de dublado PT-BR
- `custom-original-language.json` - Lingua original
- `custom-brazilian-group-tier-bad.json` - Grupos ruins PT-BR
- `custom-us-group-tier-premium.json` - Grupos premium US

**Release Quality (por app):**
- `{radarr,sonarr}-uhd-remux-release.json` - UHD Remux
- `{radarr,sonarr}-fhd-remux-release.json` - FHD Remux
- `{radarr,sonarr}-uhd-bluray-release.json` - UHD Bluray
- `{radarr,sonarr}-fhd-bluray-release.json` - FHD Bluray
- `{radarr,sonarr}-uhd-web-release.json` - UHD Web
- `{radarr,sonarr}-fhd-web-release.json` - FHD Web
- `{radarr,sonarr}-hd-remux-release.json` - HD Remux
- `{radarr,sonarr}-hd-bluray-release.json` - HD Bluray
- `{radarr,sonarr}-hd-web-release.json` - HD Web

**Codecs/Tags (por app):**
- `{radarr,sonarr}-custom-pt-br-globoplay.json`
- `{radarr,sonarr}-custom-pt-br-{x264,x265,h264,h265}.json`
- `sonarr-custom-season-pack.json`

> NOTA: Os antigos arquivos `custom-pt-br-*.json` (dual-audio, dublado, legendado, web-tier, etc.) NAO existem mais. Foram substituidos pelos `custom-brazilian-*`.

### Configs Configarr (configarr/)
3 tipos de perfis x 2 linguas x 2 anime = 12 arquivos:

**Nomenclatura:** `config-{LINGUA}-{TIPO}[-SEM-ANIMES].yaml`

**Tipos de perfil (por prioridade de qualidade):**
1. **4K-HDR** - Maximo: 4K com HDR habilitado (scores mais altos)
2. **4K** - 4K sem HDR (HDR penalizado com -10000)
3. **Base** (sem sufixo extra) - Sem 4K e sem HDR (ambos penalizados com -10000)

**Linguas:**
- **DUBLADO** - Prioriza dual-audio(30000) > dual-language(29500) > dubbed-group(25000) > dubbed(24000) > subtitles(20000)
- **LEGENDADO** - Prioriza subtitles(30000) > subtitles-detect(29500) > dubbed-group(25000) > dubbed(24000) > dual-audio(20000)

## Estrutura de Scores

### Audio Quality (igual para todos os perfis)
| Custom Format | Score |
|---|---|
| TrueHD Atmos | 5000 |
| DTS X | 4500 |
| ATMOS (undefined) | 3000 |
| DD+ ATMOS | 3000 |
| TrueHD | 2750 |
| DTS-HD MA | 2500 |
| FLAC | 2250 |
| PCM | 2250 |
| DTS-HD HRA | 2000 |
| DD+ | 1750 |
| DTS-ES | 1500 |
| DTS | 1250 |
| AAC | 1000 |
| DD (750) | 750 |
| DD (500) | 500 |
| DD (250) | 250 |

### Audio Channel (igual para todos)
Mono=1, Stereo=10, 3.0=15, 4.0=20, 5.1=25, 6.1=30, 7.1=35

### Video Quality - Variavel por perfil

**Perfil 4K-HDR e 4K (UHD habilitado):**
| Radarr | Score | Sonarr | Score |
|---|---|---|---|
| radarr-uhd-remux-release | 7000 | sonarr-uhd-remux-release | 7000 |
| radarr-fhd-remux-release | 6750 | sonarr-fhd-remux-release | 6750 |
| radarr-uhd-bluray-release | 4000 | sonarr-uhd-bluray-release | 4000 |
| radarr-fhd-bluray-release | 3500 | sonarr-fhd-bluray-release | 3500 |
| radarr-uhd-web-release | 3000 | sonarr-uhd-web-release | 3000 |
| radarr-fhd-web-release | 2500 | sonarr-fhd-web-release | 2500 |
| radarr-hd-remux-release | 2250 | sonarr-hd-remux-release | 2250 |
| radarr-hd-bluray-release | 2000 | sonarr-hd-bluray-release | 2000 |
| radarr-hd-web-release | 1750 | sonarr-hd-web-release | 1750 |

**Perfil Base (sem 4K) - UHD penalizado:**
| Release | Score |
|---|---|
| UHD Remux | -10000 |
| FHD Remux | 6750 |
| UHD Bluray | -10000 |
| FHD Bluray | 3500 |
| UHD Web | -10000 |
| FHD Web | 2500 |
| HD Remux | 2250 |
| HD Bluray | 2000 |
| HD Web | 1750 |

### HDR - Variavel por perfil

**Perfil 4K-HDR (HDR habilitado):**
| Custom Format | Score Radarr | Score Sonarr |
|---|---|---|
| HDR | 1500 | 1500 |
| DV Boost | 2500 | 2500 |
| HDR10 Plus Boost | 2000 | 2000 |
| DV (Disk) | 2500 | 2500 |
| DV (w/o HDR fallback) | -100000 | -100000 |
| Generated Dynamic HDR | -100000 | -100000 |
| SDR | 0 | 0 |
| SDR (no WEBDL) | 0 | 0 |

**Perfil 4K e Base (HDR desabilitado):**
| Custom Format | Score |
|---|---|
| HDR | -10000 |
| DV Boost | -10000 |
| HDR10 Plus Boost | -10000 |
| DV (Disk) | -10000 |
| DV (w/o HDR fallback) | -100000 |
| Generated Dynamic HDR | -100000 |
| SDR | 10 |
| SDR (no WEBDL) | 10 |

### PT-BR Tiers - Variavel por lingua

**DUBLADO (prioriza audio PT-BR):**
| Custom Format | Score Movies/Series | Score Animes |
|---|---|---|
| custom-brazilian-group-tier-dual-audio | 30000 | 30000 |
| custom-brazilian-dual-language | 29500 | 29500 |
| custom-brazilian-group-tier-dubbed | 25000 | 25000 |
| custom-brazilian-dubbed | 24000 | 24000 |
| custom-brazilian-group-tier-subtitles | 20000 | 20000 |
| custom-brazilian-subtitles | 19500 | 19500 |
| custom-original-language | 1000 | 1000 |
| custom-brazilian-group-tier-bad | 15000 | 15000 |
| custom-us-group-tier-premium | 5000 | 5000 |

**LEGENDADO (prioriza legendas PT-BR):**
| Custom Format | Score Movies/Series | Score Animes |
|---|---|---|
| custom-brazilian-group-tier-subtitles | 30000 | 30000 |
| custom-brazilian-subtitles | 29500 | 29500 |
| custom-brazilian-group-tier-dubbed | 25000 | 25000 |
| custom-brazilian-dubbed | 24000 | 24000 |
| custom-brazilian-group-tier-dual-audio | 20000 | 20000 |
| custom-brazilian-dual-language | 19500 | 19500 |
| custom-original-language | 1000 | 1000 |
| custom-brazilian-group-tier-bad | 15000 | 15000 |
| custom-us-group-tier-premium | 5000 | 5000 |

### Codecs (igual para todos)
- AV1: -10000000
- x264/x265/h264/h265: 0
- x266: -100000
- MPEG2/VC-1/VP9: 0
- INTERNAL: 0
- HFR: 0

### Bad Groups (igual para todos)
- LQ / LQ (Release Title): -100000
- Sing-Along / 3D / B&W Editions: -100000
- No-RlsGroup: 0
- Obscurated / Retags / Scene: -100000

### Streaming Services (igual para todos)
Todos score 0, exceto: BCORE=15, CRiT=15, MA=20

### Quality Profile
- Profile name: HD
- Language: Original
- Upgrade allowed: true
- Until quality: FULLHD
- Quality sort: top

### Secoes do config
Cada config tem 4 secoes (ou 2 para SEM-ANIMES):
1. **radarr.movies** - Filmes
2. **radarr.animes-movies** - Animes filme (removido em SEM-ANIMES)
3. **sonarr.series** - Series
4. **sonarr.animes-series** - Animes serie (removido em SEM-ANIMES)

### Trash IDs importantes (UUIDs do TRaSH Guides)

**HDR (Radarr):**
- 493b6d1dbec3c3364c59d7607f7e3405 = HDR
- b337d6812e06c200ec9a2d3cfa9d20a7 = DV Boost
- caa37d0df9c348912df1fb1d88f9273a = HDR10 Plus Boost
- f700d29429c023a5734505e77daeaea7 = DV (Disk)
- 923b6abef9b17f937fab56cfcf89e1f1 = DV (w/o HDR fallback)
- e6886871085226c3da1830830146846c = Generated Dynamic HDR
- 9c38ebb7384dada637be8899efa68e6f = SDR
- 25c12f78430a3a23413652cbd1d48d77 = SDR (no WEBDL)

**HDR (Sonarr):**
- 505d871304820ba7106b693be6fe4a9e = HDR
- 7c3a61a9c6cb04f52f1544be6d44a026 = DV Boost
- 0c4b99df9206d2cfac3c05ab897dd62a = HDR10 Plus Boost
- ef4963043b0987f8485bc9106f16db38 = DV (Disk)
- 9b27ab6498ec0f31a3353992e19434ca = DV (w/o HDR fallback)

**Audio (igual Radarr/Sonarr):**
- 496f355514737f7d83bf7aa4d24f8169 = TrueHD Atmos
- 2f22d89048b01681dde8afe203bf2e95 = DTS X
- (etc - veja configs para lista completa)

## Passos Realizados

1. Criar CLAUDE.md (este arquivo) com contexto completo
2. Gerar novos configs em configarr/ com 3 tipos (4K-HDR, 4K, Base)
3. Variantes DUBLADO e LEGENDADO para cada tipo
4. Variantes SEM-ANIMES para cada combinacao
5. Remover configs antigos (HDR-ON naming)
6. Atualizar k8s configarr-config.yaml
7. Atualizar README.md com nova documentacao
8. Commit e push

## Releases e Versionamento

### Branch Strategy
- **alpha** - Desenvolvimento ativo (branch de trabalho do Claude)
- **beta** - Validacao (release `latest`)
- **stable** - Producao (releases versionadas v1.0.0)
- **develop/main** - NAO TOCAR (compatibilidade com downloads existentes)

### GitHub Actions (.github/workflows/release.yml)
- Trigger: push de tag `v*.*.*` OU workflow_dispatch manual (versao + branch)
- Assets gerados: JSONs individuais, YAMLs individuais, ZIPs, docker-compose renomeados, script sh
- URLs de download:
  - Latest: `https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/ARQUIVO`
  - Versionado: `https://github.com/marcosviniciusi/trash-guides-ptbr/releases/download/vX.Y.Z/ARQUIVO`

### Download Scripts
- BASE_URL aponta para `releases/latest/download` (NAO mais para raw.githubusercontent)
- Todos os scripts (manual sh, docker-compose automatico, k8s cronjob) usam nomes `custom-brazilian-*`
- curl -fsSL com flag -L ja segue redirects do GitHub Releases (302)

## Regras de Negocio

- Score -10000 = penalizacao forte (evita download)
- Score -100000 = penalizacao severa (nunca baixar)
- Score -10000000 = bloqueio absoluto (AV1, etc)
- Scores positivos = preferencia (quanto maior, mais prioridade)
- DUBLADO prioriza audio portugues (dual-audio > legendas)
- LEGENDADO prioriza legendas (legendas > dual-audio)
- SEM-ANIMES remove secoes animes-movies e animes-series
- Base do k8s (iac/k8s/configarr/configarr-config.yaml) tem a logica correta
- Antigos custom-pt-br-*.json foram substituidos por custom-brazilian-*.json
