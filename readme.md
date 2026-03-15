# TRaSH Guides PT-BR - Custom Formats

Custom Formats em Português Brasileiro para Radarr e Sonarr, otimizados para conteúdo nacional com (DUAL-AUDIO)/legendas PT-BR e também o Dublado.

[![Configarr Compatible](https://img.shields.io/badge/Configarr-Compatible-green)](https://github.com/raydak-labs/configarr)
[![Radarr Compatible](https://img.shields.io/badge/Radarr-Compatible-green)](https://github.com/Radarr/Radarr)
[![Sonarr Compatible](https://img.shields.io/badge/Sonarr-Compatible-green)](https://github.com/Sonarr/Sonarr)
[![TRaSH-Guides Compatible](https://img.shields.io/badge/TRaSHGuides-Compatible-green)](https://github.com/TRaSH-Guides/Guides)

---

> ## ⚠️ IMPORTANTE: Branches e Releases
>
> ### 🚨 As branches `main` e `develop` NÃO serão mais atualizadas!
>
> **Todo o desenvolvimento agora acontece nas branches de release abaixo.**
> Se você estava usando `main` ou `develop`, migre para a branch `stable`.
>
> | Branch | Release | Descrição |
> |--------|---------|-----------|
> | **`stable`** | [![Stable](https://img.shields.io/badge/stable-green)](#) | **Produção** — Testado, validado e sem erros (incluindo classificação de grupos). Atualização mensal. |
> | **`beta`** | [![Beta](https://img.shields.io/badge/beta-yellow)](#) | **Pré-produção** — Validado pelo mantenedor, mas pode conter erros e classificações errôneas de grupos. |
> | **`alpha`** | [![Alpha](https://img.shields.io/badge/alpha-red)](#) | **Desenvolvimento** — Validações e testes em andamento. **Evitar usar em ambiente produtivo.** |
>
> ### Como usar a branch correta
>
> ```bash
> # Para produção (recomendado)
> git clone -b stable https://github.com/marcosviniciusi/trash-guides-ptbr.git
>
> # Para testar novidades antes de todo mundo
> git clone -b beta https://github.com/marcosviniciusi/trash-guides-ptbr.git
> ```
>
> **Downloads via Release:** cada branch gera uma release automática com todos os arquivos (JSONs, configs, ZIPs, scripts).
> Basta acessar a [página de Releases](https://github.com/marcosviniciusi/trash-guides-ptbr/releases) e escolher o canal desejado.

---

## 🌟 Apoie o Projeto

Se este projeto foi útil para você, considere:

- ⭐ Dar uma **estrela** no repositório
- 🔄 **Compartilhar** com outros usuários brasileiros de Radarr/Sonarr
- 🐛 **Reportar bugs** ou sugerir melhorias
- 🤝 **Contribuir** com novos custom formats ou melhorias na documentação

---
## 📋 Índice

- [Sobre](#-sobre)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Perfis Disponíveis](#-perfis-disponíveis)
  - [Tipos de Perfil (4K/HDR)](#tipos-de-perfil-4khdr)
  - [Línguas (Dublado/Legendado)](#línguas-dubladolegendado)
- [Custom Formats Disponíveis](#-custom-formats-disponíveis)
- [Estrutura de Scores](#-estrutura-de-scores)
  - [Video Quality (4K)](#video-quality-4k)
  - [HDR](#hdr)
  - [PT-BR Tiers](#pt-br-tiers)
- [Configurando os Quality Profiles](#-configurando-os-quality-profiles)
  - [Criando o Profile "HD"](#criando-o-profile-com-nome-hd)
- [Configurando Manualmente os custom Formats](#configurando-manualmente-os-custom-formats)
- [O que é o Configarr?](#-o-que-é-o-configarr)
  - [Vantagens](#vantagens)
  - [Como Funciona?](#como-funciona)
  - [Principais Benefícios](#-principais-benefícios)
  - [Como Configurar?](#como-configura-lo)
    - [Pré-Requisitos](#pré-requisitos)
    - [Docker Compose - Execução Manual](#docker-compose---execução-manual)
    - [Docker Compose - Execução Agendada](#docker-compose---execução-agendada-com-ofelia)
    - [Kubernetes](#️-kubernetes)
- [Atualizações Automáticas](#-atualizações-automáticas)
- [Releases e Versionamento](#-releases-e-versionamento)
- [Contribuindo](#-contribuindo)
- [FAQ](#-faq)

## 🎯 Sobre

Este repositório contém **Custom Formats personalizados** desenvolvidos especificamente para a comunidade brasileira, priorizando:

- ✅ **Conteúdo em PT-BR**: Releases Dual-Audio/Legendados/Dublados em português brasileiro
- ✅ **Grupos confiáveis**: Releases de grupos brasileiros reconhecidos
- ✅ **Qualidade otimizada**: Filtros específicos para garantir qualidade adequada
- ✅ **Foco em animes**: Formatos especializados para conteúdo japonês com PT-BR
- ✅ **Automação completa**: Compatível com Configarr para sincronização automática

> **Nota importante:** Estes formatos são **complementares** aos [TRaSH Guides oficiais](https://trash-guides.info/), não substitutos. Use ambos para obter os melhores resultados!

## Aviso Importante: 📋 Sobre a Precisão das Regras de Detecção

As regras **Not-Group** aplicadas aos perfis de **LEGENDADO** e **DUBLADO** utilizam expressões regulares genéricas para cobrir o máximo de variações possíveis.

### 🎯 Contexto Importante

Os trackers brasileiros prestam um **serviço valioso e essencial** à comunidade, disponibilizando conteúdo de qualidade em português. Reconhecemos e valorizamos profundamente este trabalho.

No entanto, devido à **ausência de padronização consistente** na nomenclatura de releases entre diferentes trackers públicos/privados, alguns desafios técnicos são inevitáveis:

- Alguns trackers utilizam terminologias específicas (e.g., "Dual Ã udio" com caracteres especiais)
- Outros não incluem o nome do release group nos títulos
- Há variações significativas nos formatos de nomenclatura entre diferentes fontes
- Alguns padrões são únicos de trackers específicos

### ⚠️ Comportamento Esperado

Devido a essa heterogeneidade natural nos padrões de nomenclatura, **falsos positivos podem ocorrer ocasionalmente** (e.g., releases legendados sendo classificados como dublados ou vice-versa).

As expressões regulares foram desenvolvidas com base em **centenas de variações observadas** e refinadas continuamente. Contudo, a natureza diversificada dos padrões impossibilita uma precisão de 100% em todos os cenários.

### 🤝 Contribuições da Comunidade

**Sua ajuda é bem-vinda!** Se você identificar novos padrões de nomenclatura, formatos específicos de trackers ou releases que não estão sendo capturados corretamente, por favor compartilhe conosco através de:

- Issues no repositório com exemplos de títulos de releases
- Pull requests com sugestões de melhorias nas regex
- Informações sobre novos release groups brasileiros

Quanto mais informações a comunidade compartilhar, melhor será a cobertura dos custom formats para capturar o máximo de releases possíveis! 🚀

---

*Agradecemos aos trackers brasileiros pelo trabalho contínuo em disponibilizar conteúdo de qualidade à comunidade!* 🇧🇷

## 📁 Estrutura do Repositório

```
trash-guides-ptbr/
├── README.md
├── CLAUDE.md                                          # Contexto e documentação técnica
├── configarr/                                         # Configs Configarr (3 perfis x 2 línguas x 2 anime)
│   ├── config-DUBLADO-4K-HDR.yaml                     # DUBLADO: 4K + HDR (scores máximos)
│   ├── config-DUBLADO-4K-HDR-SEM-ANIMES.yaml          # DUBLADO: 4K + HDR sem animes
│   ├── config-DUBLADO-4K.yaml                         # DUBLADO: 4K sem HDR (HDR = -10000)
│   ├── config-DUBLADO-4K-SEM-ANIMES.yaml              # DUBLADO: 4K sem HDR sem animes
│   ├── config-DUBLADO.yaml                            # DUBLADO: Sem 4K e sem HDR (ambos = -10000)
│   ├── config-DUBLADO-SEM-ANIMES.yaml                 # DUBLADO: Sem 4K/HDR sem animes
│   ├── config-LEGENDADO-4K-HDR.yaml                   # LEGENDADO: 4K + HDR (scores máximos)
│   ├── config-LEGENDADO-4K-HDR-SEM-ANIMES.yaml        # LEGENDADO: 4K + HDR sem animes
│   ├── config-LEGENDADO-4K.yaml                       # LEGENDADO: 4K sem HDR (HDR = -10000)
│   ├── config-LEGENDADO-4K-SEM-ANIMES.yaml            # LEGENDADO: 4K sem HDR sem animes
│   ├── config-LEGENDADO.yaml                          # LEGENDADO: Sem 4K e sem HDR (ambos = -10000)
│   ├── config-LEGENDADO-SEM-ANIMES.yaml               # LEGENDADO: Sem 4K/HDR sem animes
│   └── config-profile-EXAMPLE.yaml                    # Template de exemplo
├── custom-formats/                                    # Todos os custom formats
│   │   # PT-BR Específicos
│   ├── custom-brazilian-group-tier-dual-audio.json     # Grupos PT-BR com Dual Audio
│   ├── custom-brazilian-dual-language.json             # Detecção Dual Language
│   ├── custom-brazilian-group-tier-subtitles.json      # Grupos PT-BR com Legendas
│   ├── custom-brazilian-subtitles.json                 # Detecção Legendas PT-BR
│   ├── custom-brazilian-group-tier-dubbed.json         # Grupos PT-BR com Dublagem
│   ├── custom-brazilian-dubbed.json                    # Detecção Dublado PT-BR
│   ├── custom-original-language.json                   # Língua Original
│   ├── custom-brazilian-group-tier-bad.json            # Grupos Não Confiáveis
│   ├── custom-us-group-tier-premium.json               # Grupos Premium US
│   │   # Release Quality (Radarr)
│   ├── radarr-uhd-remux-release.json                   # UHD Remux
│   ├── radarr-fhd-remux-release.json                   # FHD Remux
│   ├── radarr-uhd-bluray-release.json                  # UHD Bluray
│   ├── radarr-fhd-bluray-release.json                  # FHD Bluray
│   ├── radarr-uhd-web-release.json                     # UHD Web
│   ├── radarr-fhd-web-release.json                     # FHD Web
│   ├── radarr-hd-{remux,bluray,web}-release.json       # HD variants
│   │   # Release Quality (Sonarr)
│   ├── sonarr-{uhd,fhd,hd}-{remux,bluray,web}-release.json
│   │   # Tags/Codecs (por app)
│   ├── {radarr,sonarr}-custom-pt-br-globoplay.json     # Tag GloboPlay
│   ├── {radarr,sonarr}-custom-pt-br-{x264,x265,h264,h265}.json  # Tags Encoder
│   └── sonarr-custom-season-pack.json                  # Season Pack
├── iac/                                               # Infraestrutura como Código
│   ├── docker-compose/
│   │   ├── automatico/
│   │   │   └── docker-compose.yaml                    # Docker Compose Automático
│   │   └── manual/
│   │       ├── docker-compose.yaml                    # Docker Compose Manual
│   │       └── download-custom-formats.sh             # Script Downloads Custom Formats
│   └── k8s/
│       └── configarr/                                 # Manifestos Kubernetes
│           ├── configarr-config.yaml                   # ConfigMap (base de referência)
│           ├── configarr-cronjob.yaml
│           ├── configarr-pvc.yaml
│           ├── configarr-secrets.yaml
│           └── kustomization.yaml
└── prowlarr-indexes/                                  # Indexes do Prowlarr Modificados
    ├── amigosshare-trashguides-ptbr.yml               # AmigosShare
    ├── bjshare-trashguides-ptbr.yml                   # BJShare
    ├── brasiltracker-trashguides-ptbr.yml             # BrasilTracker
    ├── shakaw-cookie.yaml                             # Shakaw (cookie auth)
    └── shakaw-trashguides-ptbr.yml                    # Shakaw
```

## 🎬 Perfis Disponíveis

### Tipos de Perfil (4K/HDR)

Existem **3 tipos de perfil** que controlam o comportamento de 4K e HDR:

| Perfil | 4K/UHD | HDR | Descrição |
|--------|--------|-----|-----------|
| **4K-HDR** | Scores altos (UHD Remux=7000) | Scores positivos (HDR=1500, DV=2500) | Qualidade máxima com 4K e HDR |
| **4K** | Scores altos (UHD Remux=7000) | Score -10000 (penalizado) | 4K sem HDR - evita conteúdo HDR |
| **Base** (sem sufixo) | Score -10000 (penalizado) | Score -10000 (penalizado) | Sem 4K e sem HDR - apenas HD/FHD |

### Línguas (Dublado/Legendado)

| Língua | Prioridade | Descrição |
|--------|-----------|-----------|
| **DUBLADO** | Dual Audio (30000) > Dubbed Group (25000) > Dubbed (24000) | Áudio em português, sem legendado |
| **LEGENDADO** | Dual Audio (30000) > Legendas (25000) > Legendas Detect (24000) | Legendas em português, sem dublado |

### Combinações Disponíveis

Cada tipo + língua possui variante **COM** e **SEM ANIMES** (12 configs total):

| Config | Tipo | Língua |
|--------|------|--------|
| `config-DUBLADO-4K-HDR.yaml` | 4K + HDR | Dublado |
| `config-DUBLADO-4K.yaml` | 4K sem HDR | Dublado |
| `config-DUBLADO.yaml` | Sem 4K/HDR | Dublado |
| `config-LEGENDADO-4K-HDR.yaml` | 4K + HDR | Legendado |
| `config-LEGENDADO-4K.yaml` | 4K sem HDR | Legendado |
| `config-LEGENDADO.yaml` | Sem 4K/HDR | Legendado |

> Todas as combinações acima possuem variante `-SEM-ANIMES` (ex: `config-DUBLADO-4K-HDR-SEM-ANIMES.yaml`)

---

# 📦 Custom Formats Disponíveis

### PT-BR Específicos

| Custom Format | Descrição | Score DUBLADO | Score LEGENDADO |
|---------------|-----------|---------------|-----------------|
| **custom-brazilian-group-tier-dual-audio** | Grupos PT-BR com Dual Audio | +30000 | +30000 |
| **custom-brazilian-dual-language** | Detecção Dual Language | +29500 | +29500 |
| **custom-brazilian-group-tier-dubbed** | Grupos PT-BR com Dublagem | +25000 | - |
| **custom-brazilian-dubbed** | Detecção Dublado PT-BR | +24000 | - |
| **custom-brazilian-group-tier-subtitles** | Grupos PT-BR com Legendas | - | +25000 |
| **custom-brazilian-subtitles** | Detecção Legendas PT-BR | - | +24000 |
| **custom-original-language** | Língua Original | +1000 | +1000 |
| **custom-brazilian-group-tier-bad** | Grupos Não Confiáveis | +15000 | +15000 |
| **custom-us-group-tier-premium** | Grupos Premium US | +5000 | +5000 |

### Release Quality (por app)

| Custom Format | Descrição | Score 4K/4K-HDR | Score Base |
|---------------|-----------|-----------------|-----------|
| **{radarr,sonarr}-uhd-remux-release** | UHD Remux | +7000 | -10000 |
| **{radarr,sonarr}-fhd-remux-release** | FHD Remux | +6750 | +6750 |
| **{radarr,sonarr}-uhd-bluray-release** | UHD Bluray | +4000 | -10000 |
| **{radarr,sonarr}-fhd-bluray-release** | FHD Bluray | +3500 | +3500 |
| **{radarr,sonarr}-uhd-web-release** | UHD Web | +3000 | -10000 |
| **{radarr,sonarr}-fhd-web-release** | FHD Web | +2500 | +2500 |
| **{radarr,sonarr}-hd-remux-release** | HD Remux | +2250 | +2250 |
| **{radarr,sonarr}-hd-bluray-release** | HD Bluray | +2000 | +2000 |
| **{radarr,sonarr}-hd-web-release** | HD Web | +1750 | +1750 |

### Tags/Codecs

| Custom Format | Descrição | Score |
|---------------|-----------|-------|
| **{radarr,sonarr}-custom-pt-br-globoplay** | Tag GloboPlay | 0 |
| **{radarr,sonarr}-custom-pt-br-{x264,x265,h264,h265}** | Tags Encoder | 0 |
| **sonarr-custom-season-pack** | Season Pack | 0 |

- **Tag Encoders** somente se precisar de scores específicos ou distinguir entre software (x264/x265) e hardware (H.264/H.265).
- **Custom Formats exclusivos do Radarr/Sonarr**: Aqueles prefixados com "radarr" ou "sonarr" devem ser utilizados apenas em seu respectivo programa.

## 📊 Estrutura de Scores

### Video Quality (4K)

Os scores de Video Quality controlam a preferência por conteúdo UHD/4K vs HD/FHD:

| Release Type | Perfil 4K-HDR / 4K | Perfil Base (sem 4K) |
|---|---|---|
| UHD Remux | +7000 | **-10000** |
| FHD Remux | +6750 | +6750 |
| UHD Bluray | +4000 | **-10000** |
| FHD Bluray | +3500 | +3500 |
| UHD Web | +3000 | **-10000** |
| FHD Web | +2500 | +2500 |
| HD Remux | +2250 | +2250 |
| HD Bluray | +2000 | +2000 |
| HD Web | +1750 | +1750 |

### HDR

| Custom Format | Perfil 4K-HDR | Perfil 4K / Base |
|---|---|---|
| HDR | +1500 | **-10000** |
| DV Boost | +2500 | **-10000** |
| HDR10 Plus Boost | +2000 | **-10000** |
| DV (Disk) | +2500 | **-10000** |
| DV (w/o HDR fallback) | -100000 | -100000 |
| Generated Dynamic HDR | -100000 | -100000 |
| SDR | 0 | +10 |
| SDR (no WEBDL) | 0 | +10 |

### PT-BR Tiers

| Custom Format | DUBLADO | LEGENDADO |
|---|---|---|
| Grupos Dual Audio | +30000 | +30000 |
| Dual Language | +29500 | +29500 |
| Grupos Dubbed | +25000 | - |
| Dubbed | +24000 | - |
| Grupos Legendas | - | +25000 |
| Legendas PT-BR | - | +24000 |
| Língua Original | +1000 | +1000 |
| Grupos Ruins | +15000 | +15000 |
| Grupos Premium US | +5000 | +5000 |

### Audio Quality (igual para todos os perfis)

| Codec | Score |
|---|---|
| TrueHD Atmos | +5000 |
| DTS X | +4500 |
| ATMOS (undefined) / DD+ ATMOS | +3000 |
| TrueHD | +2750 |
| DTS-HD MA | +2500 |
| FLAC / PCM | +2250 |
| DTS-HD HRA | +2000 |
| DD+ | +1750 |
| DTS-ES | +1500 |
| DTS | +1250 |
| AAC | +1000 |

---

## 🔧 Configurando os Quality Profiles

### Pré-requisito: Criar Quality Profile "HD"

Antes de configurar os custom formats, você precisa ter um Quality Profile chamado **"HD"** (ou ajustar o nome no `config.yml`).

### Criando o Profile com Nome "HD"

#### No Radarr/Sonarr:

1. Acesse **Settings -> Profiles**
2. Clique em **+** para adicionar novo perfil
3. Configure:
   - **Name**: `HD`
   - **Upgrades Allowed**: Habilitado
   - **Upgrade Until**: FULLHD
   - **Qualities**: Bluray-2160p, WEBDL-2160p, WEBRip-2160p, Bluray-1080p, WEBDL-1080p, WEBRip-1080p (ajuste conforme o perfil)
   - **Minimum Custom Format Score** Recomendado:
      - Filmes/Series Mix de Conteudos Gringos mas que prefira PT-BR: 250 (caso tenha um Bazarr configurado)
      - Filmes/Series Apenas Dual Audio/Legendados: 7500
      - Filmes/Series Apenas Dual Audio/Dublado: 7500
      - Animes GLOBAL Apenas Dual Audio/Legendado/Dublados: 19000
   - **Upgrade Until Custom Format Score** Recomendado:
      - Filmes/Series Sem HDR: 23100
      - Filmes/Series Com HDR: 24500
      - Animes: 60000
4. Clique em **Save**

## **Pré-Requisito OBRIGATÓRIO:** Estrutura de Nomeação dos Arquivos

### Por que essa configuração é essencial?

A nomeação dos arquivos no Radarr e Sonarr é o que permite que todo o sistema de Custom Formats funcione corretamente. Sem ela, os scores não são aplicados e a automação perde o sentido.

Os formatos abaixo utilizam duas tags fundamentais:

| Tag no nome do arquivo | O que faz |
|------------------------|-----------|
| `[audio-{MediaInfo-AudioLanguages}]` | Grava no nome do arquivo **todos os idiomas de áudio** detectados pelo MediaInfo (ex: `[audio-Portuguese Brazilian English]`) |
| `[subs-{MediaInfo-SubtitleLanguages:PT}]` | Grava no nome do arquivo **todas as legendas embutidas** em Português detectadas pelo MediaInfo (ex: `[subs-[PT]]`) |

### Detecção automática de áudio e legendas PT-BR

Com essas tags, o Radarr/Sonarr **analisa o conteúdo real do arquivo** (via MediaInfo) após o download e inclui as informações de idioma diretamente no nome. Isso permite que os Custom Formats identifiquem automaticamente:

- **Áudio em PT-BR** — O Custom Format de `dubbed` detecta quando o arquivo contém trilha de áudio em português, mesmo que o release não tenha sido publicado por um grupo brasileiro. O score de dublado é aplicado corretamente.
- **Legendas embutidas em PT-BR** — O Custom Format de `subtitles` detecta quando o arquivo contém legendas em português embutidas (não externas). O score de legendado é aplicado corretamente.
- **Dual Audio** — Quando o arquivo contém **tanto** áudio original quanto áudio em português, os Custom Formats de `dual-audio` e `dual-language` identificam e aplicam o score máximo.

### Evitando Race Condition

É comum que **grupos internacionais** (gringos) publiquem releases que já incluem áudio ou legendas em PT-BR embutidos — muitas vezes sem mencionar isso no título original do release. Sem a nomeação correta, o seguinte problema acontece:

```
1. Radarr/Sonarr baixa o release "Movie.2024.1080p.BluRay.x264-GrupoGringo"
2. O título não menciona PT-BR → Custom Formats não aplicam score de idioma
3. Radarr/Sonarr encontra outro release e faz upgrade desnecessário
4. Ou pior: descarta um release que já tinha PT-BR em favor de um sem
```

Com a nomeação configurada, o fluxo correto é:

```
1. Radarr/Sonarr baixa o release
2. Após a importação, MediaInfo analisa o arquivo real
3. Detecta áudio PT-BR e/ou legendas PT-BR embutidas
4. Renomeia o arquivo incluindo [audio-...] e [subs-...]
5. Custom Formats reanalisam e aplicam os scores corretos
6. O release recebe a pontuação adequada → sem upgrades desnecessários
```

> **Resumo:** A nomeação correta garante que a pontuação dos Custom Formats reflita o **conteúdo real do arquivo**, e não apenas o que o título do release diz. Isso evita upgrades desnecessários e garante que releases com PT-BR embutido sejam corretamente valorizados.

---

***Configurando os formatos de arquivos:***

#### Radarr (Filmes e Animes)

```
#Formato do Filme
{Movie-CleanTitle}-{(Release-Year)}[imdbid-{ImdbId}]{[Quality-Title]}{[CUSTOM-FORMATS]}{[MediaInfo-3D]}{[MediaInfo-VideoDynamicRangeType]}{[Mediainfo-AudioCodec}{Mediainfo-AudioChannels]}{[Mediainfo-VideoCodec]}[audio-{MediaInfo-AudioLanguages}][subs-{MediaInfo-SubtitleLanguages:PT}]{-Release_Group}
```
```
#Formato da Pasta do Filme
{Movie CleanTitle}_({Release Year})_[imdbid-{ImdbId}]
```

#### Sonarr (Series e Animes)

```
#Formato do Episodio Padrao
S{season:00}E{episode:00}-{absolute:000}-[imdb-{ImdbId}]-[{Quality-Title}]{[MediaInfo-VideoDynamicRangeType]}{[CUSTOM-FORMATS]}[{MediaInfo-VideoBitDepth}bit]{[MediaInfo-VideoCodec]}[{Mediainfo-AudioCodec}{Mediainfo-AudioChannels}][audio-{MediaInfo-AudioLanguages}][subs-{MediaInfo-SubtitleLanguages:PT}]{-Release_Group}
```
```
#Formato do Episodio Diario
S{season:00}E{episode:00}-{absolute:000}-[imdb-{ImdbId}]-[{Quality-Title}]{[MediaInfo-VideoDynamicRangeType]}{[CUSTOM-FORMATS]}[{MediaInfo-VideoBitDepth}bit]{[MediaInfo-VideoCodec]}[{Mediainfo-AudioCodec}{Mediainfo-AudioChannels}][audio-{MediaInfo-AudioLanguages}][subs-{MediaInfo-SubtitleLanguages:PT}]{-Release_Group}
```
```
#Formato do Episodio de Anime
S{season:00}E{episode:00}-{absolute:000}-[imdb-{ImdbId}]-[{Quality-Title}]{[MediaInfo-VideoDynamicRangeType]}{[CUSTOM-FORMATS]}[{MediaInfo-VideoBitDepth}bit]{[MediaInfo-VideoCodec]}[{Mediainfo-AudioCodec}{Mediainfo-AudioChannels}][audio-{MediaInfo-AudioLanguages}][subs-{MediaInfo-SubtitleLanguages:PT}]{-Release_Group}
```
```
#Formato de Pasta das Series
{Series_TitleYear}-[imdb-{ImdbId}]
```
```
#Formato da Pasta da Temporada
Season {season:00}
```
```
#Formato da Pasta para Especiais
Specials
```

## Habilite "Mostrar Opções Avançadas" na mesma pagina ao topo e configure os seguintes campos abaixo:

-  **"Importar Arquivos adicionais"** e adicine estes valores:
```
srt,nfo,sub,ass,ssa
```

-  **"Analisar Arquivos de Videos"**

-  **"Verificar Novamente a Pasta do Filme/Serie Após Atualização"** para **"SEMPRE"**.



## 🔍 Por que os Indexes Customizados do Prowlarr?

Os Custom Formats do Radarr/Sonarr identificam releases brasileiros através de **palavras-chave padronizadas** no título (ex: `BRAZILIAN-DUAL-AUDIO`, `DUBLADO`, `LEGENDADO`). Porém, cada tracker brasileiro usa sua própria convenção de nomenclatura:

| Tracker | Exemplo de título original |
|---------|---------------------------|
| Tracker A | `Filme.2024.DUAL.1080p` |
| Tracker B | `Filme (2024) Dual Áudio 1080p` |
| Tracker C | `Filme.2024.Nacional.1080p` |

Sem padronização, o Radarr/Sonarr **não consegue identificar corretamente** se um release é dual audio, dublado ou legendado, e os scores dos Custom Formats não são aplicados.

Os indexes customizados na pasta `prowlarr-indexes/` resolvem isso: eles **padronizam os títulos antes de chegarem ao Radarr/Sonarr**, sem alterar o conteúdo ou a estrutura dos releases.

| Original no tracker | Padronizado para o Radarr/Sonarr |
|---------------------|----------------------------------|
| `DUAL`, `Dual Áudio`, `Dual Audio` | `BRAZILIAN-DUAL-AUDIO` |
| `Dublado`, `DUB` | `DUBLADO` |
| `Nacional` | `NACIONAL` |
| `Legendado`, `LEG` | `LEGENDADO` |

> **Importante:** Os indexes apenas alteram a forma como o título é **apresentado** ao Radarr/Sonarr. Nenhum conteúdo, link ou estrutura do tracker é modificado.

### Trackers suportados

| Arquivo | Tracker |
|---------|---------|
| `amigosshare-trashguides-ptbr.yml` | AmigosShare |
| `bjshare-trashguides-ptbr.yml` | BJShare |
| `brasiltracker-trashguides-ptbr.yml` | BrasilTracker |
| `shakaw-trashguides-ptbr.yml` | Shakaw |
| `shakaw-cookie.yaml` | Shakaw (autenticacao via cookie) |

### Instalacao dos Indexes

1. Localize a pasta de definicoes customizadas do Prowlarr:
```bash
# Docker
/config/Definitions/Custom

# Windows
C:\ProgramData\Prowlarr\Definitions\Custom

# Linux
~/.config/Prowlarr/Definitions/Custom
```
> Se a pasta `Custom` nao existir, crie manualmente.

2. Copie os arquivos `.yml` da pasta `prowlarr-indexes/` para esse diretorio.

3. Reinicie o Prowlarr:
```bash
docker restart prowlarr
```

4. No Prowlarr, acesse **Indexers** → **Add Indexer** e procure pelos nomes com sufixo `trashguides-ptbr`. Desative os indexers padrao equivalentes para evitar duplicacao.

> **Agradecimento:** Nosso reconhecimento a todas as comunidades de trackers brasileiros pelo trabalho continuo e dedicado. Estes indexes apenas adicionam uma camada de padronizacao tecnica para facilitar a automacao.

## Configurando Manualmente os custom Formats
## obs: siga apenas este passo se não deseja o uso do configarr.
#### No Radarr/Sonarr:

1. Acesse **Settings → Custom Formats**
2. Clique em **+** para adicionar novo formato
3. Cole o conteúdo do JSON desejado (disponível na pasta `custom-formats/`)
4. Salve e configure o score no Quality Profile correspondente
---

---

## 🤖 O que é o Configarr?

[Configarr](https://github.com/raydak-labs/configarr) é uma ferramenta de automação e sincronização para Radarr e Sonarr que permite gerenciar **Custom Formats**, **Quality Definitions** e **Quality Profiles** através de arquivos de configuração YAML.

### Vantagens?

**Configuração pronta para usar:** O `config.yaml` do repositório já inclui os **TRaSH Guides completos** integrados com nossos custom formats PT-BR. Ele configura automaticamente filtros de qualidade (áudio, HDR, codecs, etc.) e aplica os scores recomendados, eliminando toda a configuração manual e garantindo uma experiência otimizada desde o primeiro uso.

### Como funciona?

Em vez de configurar manualmente cada Custom Format pela interface web (copiando e colando JSONs um por um), o Configarr:

1. 📥 **Lê** um arquivo de configuração centralizado (`config.yml`)
2. 🔍 **Busca** os Custom Formats especificados (localmente ou de repositórios remotos)
3. 🔄 **Sincroniza** automaticamente com suas instâncias do Radarr/Sonarr
4. 🎯 **Aplica** os scores definidos nos Quality Profiles
5. ✅ **Atualiza** tudo de forma idempotente (pode executar quantas vezes quiser)
6. 🚀 **Integração TRaSH Guides**: Configuração já inclui os guides oficiais completos

### 🎯 Principais Benefícios

#### 1. **Configuração como Código (IaC)**

```yaml
# Tudo em um arquivo config.yml versionável
radarr:
  movies:
    base_url: !secret RADARR_URL
    api_key: !secret RADARR_API_KEY
    
    custom_formats:
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
        assign_scores_to:
          - name: HD
            score: 12000
```

**Benefícios:**
- ✅ Versionamento com Git
- ✅ Fácil de fazer backup
- ✅ Documentação integrada
- ✅ Reproduzível em qualquer ambiente
- ✅ Auditável e reversível

#### 2. **Sincronização Automática**

**Sem Configarr:**
```
1. Baixar JSON manualmente
2. Abrir Radarr → Settings → Custom Formats
3. Clicar em "+"
4. Copiar e colar o JSON
5. Salvar
6. Abrir Settings → Profiles
7. Rolar até encontrar o Custom Format
8. Digitar o score manualmente
9. Salvar
10. Repetir para cada Custom Format (15x? 20x? 30x? 😫)
```

**Com Configarr:**
```bash
docker run ghcr.io/raydak-labs/configarr:latest
# Pronto! ✨
```

#### 3. **O que o `config.yaml` já inclui:**

- ✅ **TRaSH Guides completos** integrados
- ✅ **Custom Formats PT-BR** para priorizar conteúdo nacional
- ✅ **Filtros automáticos** de qualidade (áudio multicanal, HDR, codecs, bitrate)
- ✅ **Scores pré-configurados** para todos os profiles
- ✅ **Zero configuração manual** - funciona imediatamente após deploy

---

## Como Configura-lo?

### Pré-requisitos

- [Criar o Profile com o nome "HD"](#criando-o-profile-com-nome-hd)
- API Keys do Radarr/Sonarr (encontradas em Settings → General → Security)
- Docker ou Kubernetes instalado

---


## Docker Compose - Execução Manual
### 1. Estrutura de Diretórios

```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/docker-compose-manual.yaml -o docker-compose.yaml
```
Obs: Ja efetua o download do docker compose. e também ja tem criado o script para baixar os custom formats, caso queira baixa-lo, use este script abaixo:

```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/docker-compose-manual.yaml -o docker-compose.yaml

#Script de Download dos Custom Formats
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/download-custom-formats.sh -o download-custom-formats.sh

chmod +x download-custom-formats.sh
./download-custom-formats.sh
```
Obs 2: Se seguir o este segundo script, Siga os passos 2 e 3, poderá ir direto a esta [Passo de execuçãp](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#5-executar).

### 2. Criar secrets.yml 
#### Completo
```bash
cat > secrets/secrets.yml << 'EOF'
SONARR_URL: "http://sonarr:8989"
RADARR_URL: "http://radarr:7878"
SONARR_ANIMES_URL: "http://sonarr-animes:8990"
RADARR_ANIMES_URL: "http://radarr-animes:7879"

SONARR_API_KEY: "sua-api-key-aqui"
RADARR_API_KEY: "sua-api-key-aqui"
SONARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
RADARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
EOF
```

#### Sem Animes
```bash
cat > secrets/secrets.yml << 'EOF'
SONARR_URL: "http://sonarr:8989"
RADARR_URL: "http://radarr:7878"

SONARR_API_KEY: "sua-api-key-aqui"
RADARR_API_KEY: "sua-api-key-aqui"
EOF
```
> **Dica:** Substitua `sonarr`, `radarr`, etc. pelos nomes reais dos seus containers/serviços.

### 3. Baixar config.yml com todos Custom Formats do trashguide e Scores
> **Dica:** Baixe apenas UM config.yaml, de acordo com o perfil desejado. Cada perfil combina tipo (4K/HDR) + lingua (Dublado/Legendado).

```bash
# ==================== DUBLADO ====================

# Opção 1: DUBLADO - 4K + HDR (qualidade máxima)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO-4K-HDR.yaml \
  -o config/config.yml

# Opção 2: DUBLADO - 4K sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO-4K.yaml \
  -o config/config.yml

# Opção 3: DUBLADO - Sem 4K e sem HDR (apenas HD/FHD)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO.yaml \
  -o config/config.yml

# ==================== LEGENDADO ====================

# Opção 4: LEGENDADO - 4K + HDR (qualidade máxima)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO-4K-HDR.yaml \
  -o config/config.yml

# Opção 5: LEGENDADO - 4K sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO-4K.yaml \
  -o config/config.yml

# Opção 6: LEGENDADO - Sem 4K e sem HDR (apenas HD/FHD)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO.yaml \
  -o config/config.yml

# ==================== SEM ANIMES ====================
# Adicione "-SEM-ANIMES" ao nome do arquivo para versões sem seções de anime.
# Exemplo:
# config-DUBLADO-4K-HDR-SEM-ANIMES.yaml
# config-LEGENDADO-4K-SEM-ANIMES.yaml
# config-DUBLADO-SEM-ANIMES.yaml
# etc.
```

**Ou crie manualmente (exemplo simplificado):**

```yaml
localCustomFormatsPath: /config/custom_formats
telemetry: true

radarr:
  movies:
    base_url: !secret RADARR_URL
    api_key: !secret RADARR_API_KEY
    
    quality_definition:
      type: movie
    
    custom_formats:
      # TRaSH Guides oficiais (incluídos automaticamente)
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
          - custom-web-tier-ptbr-not-group-radarr
        assign_scores_to:
          - name: HD
            score: 12000

sonarr:
  series:
    base_url: !secret SONARR_URL
    api_key: !secret SONARR_API_KEY
    
    quality_definition:
      type: series
    
    custom_formats:
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
          - custom-web-tier-ptbr-not-group-sonarr
        assign_scores_to:
          - name: HD
            score: 12000

# [Veja config.yml completo no repositório]
```

### 4. Script de Download dos Custom Formats

```bash
cat > download-custom-formats.sh << 'EOF'
#!/bin/bash

BASE_URL="https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download"

echo "📥 Baixando custom formats..."
# Função para baixar com tratamento de erro
download_format() {
    local file=$1
    echo "  → $file"
    curl -fsSL "$BASE_URL/$file" -o "custom_formats/$file" || {
        echo "❌ Erro ao baixar $file"
        return 1
    }
}

# Idioma PT-BR
download_format 'custom-brazilian-group-tier-dual-audio.json'
download_format 'custom-brazilian-dual-language.json'
download_format 'custom-brazilian-group-tier-subtitles.json'
download_format 'custom-brazilian-subtitles.json'
download_format 'custom-brazilian-group-tier-dubbed.json'
download_format 'custom-brazilian-dubbed.json'
download_format 'custom-original-language.json'
download_format 'custom-brazilian-group-tier-bad.json'
download_format 'custom-us-group-tier-premium.json'
# Plataformas
download_format 'sonarr-custom-pt-br-globoplay.json'
download_format 'radarr-custom-pt-br-globoplay.json'
# Codec
download_format 'radarr-custom-pt-br-x264.json'
download_format 'radarr-custom-pt-br-x265.json'
download_format 'radarr-custom-pt-br-h264.json'
download_format 'radarr-custom-pt-br-h265.json'
download_format 'sonarr-custom-pt-br-x264.json'
download_format 'sonarr-custom-pt-br-x265.json'
download_format 'sonarr-custom-pt-br-h264.json'
download_format 'sonarr-custom-pt-br-h265.json'
# Season Pack
download_format 'sonarr-custom-season-pack.json'
# Release Quality - Radarr
download_format 'radarr-uhd-remux-release.json'
download_format 'radarr-fhd-remux-release.json'
download_format 'radarr-hd-remux-release.json'
download_format 'radarr-uhd-bluray-release.json'
download_format 'radarr-fhd-bluray-release.json'
download_format 'radarr-hd-bluray-release.json'
download_format 'radarr-uhd-web-release.json'
download_format 'radarr-fhd-web-release.json'
download_format 'radarr-hd-web-release.json'
# Release Quality - Sonarr
download_format 'sonarr-uhd-remux-release.json'
download_format 'sonarr-fhd-remux-release.json'
download_format 'sonarr-hd-remux-release.json'
download_format 'sonarr-uhd-bluray-release.json'
download_format 'sonarr-fhd-bluray-release.json'
download_format 'sonarr-hd-bluray-release.json'
download_format 'sonarr-uhd-web-release.json'
download_format 'sonarr-fhd-web-release.json'
download_format 'sonarr-hd-web-release.json'

echo "✅ Custom formats baixados com sucesso!"
EOF

chmod +x download-custom-formats.sh
./download-custom-formats.sh
```

### 5. Docker Compose

```yaml
version: '3.8'

services:
  configarr:
    image: ghcr.io/raydak-labs/configarr:latest
    container_name: configarr
    volumes:
      - ./config/config.yml:/app/config/config.yml:ro
      - ./secrets/secrets.yml:/app/config/secrets.yml:ro
      - ./custom_formats:/config/custom_formats:ro
      - app-data:/app/repos
    environment:
      - LOG_STACKTRACE=true
      - OTEL_LOG_LEVEL=debug
    network_mode: bridge
    # Remove restart para execução manual
    # Use: docker-compose up configarr

volumes:
  app-data:
```

## Docker Compose - Execução Agendada (com Ofelia)
### 1. Estrutura de Diretórios

```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/docker-compose-automatico.yaml -o docker-compose.yaml
```
Obs: O script acima efetua o download do arquivo docker-compose.yaml, siga os passos 2 e 3, poderá ir direto a esta [Passo de execuçãp](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#5-executar).
### 2. Criar secrets.yml

#### Completo
```bash
cat > secrets/secrets.yml << 'EOF'
SONARR_URL: "http://sonarr:8989"
RADARR_URL: "http://radarr:7878"
SONARR_ANIMES_URL: "http://sonarr-animes:8990"
RADARR_ANIMES_URL: "http://radarr-animes:7879"

SONARR_API_KEY: "sua-api-key-aqui"
RADARR_API_KEY: "sua-api-key-aqui"
SONARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
RADARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
EOF
```

#### Sem Animes
```bash
cat > secrets/secrets.yml << 'EOF'
SONARR_URL: "http://sonarr:8989"
RADARR_URL: "http://radarr:7878"

SONARR_API_KEY: "sua-api-key-aqui"
RADARR_API_KEY: "sua-api-key-aqui"
EOF
```

> **Dica:** Substitua `sonarr`, `radarr`, etc. pelos nomes reais dos seus containers/serviços.
### 3. Baixar config.yml com todos Custom Formats do trashguide e Scores

```bash
# ==================== DUBLADO ====================

# DUBLADO - 4K + HDR (qualidade máxima)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO-4K-HDR.yaml \
  -o config/config.yml

# DUBLADO - 4K sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO-4K.yaml \
  -o config/config.yml

# DUBLADO - Sem 4K e sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-DUBLADO.yaml \
  -o config/config.yml

# ==================== LEGENDADO ====================

# LEGENDADO - 4K + HDR (qualidade máxima)
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO-4K-HDR.yaml \
  -o config/config.yml

# LEGENDADO - 4K sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO-4K.yaml \
  -o config/config.yml

# LEGENDADO - Sem 4K e sem HDR
curl -fsSL https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/config-LEGENDADO.yaml \
  -o config/config.yml

# ==================== SEM ANIMES ====================
# Adicione "-SEM-ANIMES" ao nome para versões sem anime.
# Ex: config-DUBLADO-4K-HDR-SEM-ANIMES.yaml
```

**Ou crie manualmente (exemplo simplificado):**

```yaml
localCustomFormatsPath: /config/custom_formats
telemetry: true

radarr:
  movies:
    base_url: !secret RADARR_URL
    api_key: !secret RADARR_API_KEY
    
    quality_definition:
      type: movie
    
    custom_formats:
      # TRaSH Guides oficiais (incluídos automaticamente)
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
          - custom-web-tier-ptbr-not-group-radarr
        assign_scores_to:
          - name: HD
            score: 12000

sonarr:
  series:
    base_url: !secret SONARR_URL
    api_key: !secret SONARR_API_KEY
    
    quality_definition:
      type: series
    
    custom_formats:
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
          - custom-web-tier-ptbr-not-group-sonarr
        assign_scores_to:
          - name: HD
            score: 12000

# [Veja config.yml completo no repositório]
```
### 4. Criar IAC com automatização
Para sincronização automática dos custom formats e execução agendada:

```yaml
version: '3.8'

services:
  # Download automático dos Custom Formats
  download-formats:
    image: curlimages/curl:latest
    container_name: configarr-download
    command: >
      sh -c "
      BASE_URL='https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download'

      mkdir -p /config/custom_formats

      echo '📥 Baixando custom formats...'

      download_format() {
          local file=$$1
          echo '  → '$$file
          curl -fsSL \"$$BASE_URL/$$file\" -o \"/config/custom_formats/$$file\" || {
              echo '❌ Erro ao baixar '$$file
              return 1
          }
      }

      # Idioma PT-BR
      download_format 'custom-brazilian-group-tier-dual-audio.json'
      download_format 'custom-brazilian-dual-language.json'
      download_format 'custom-brazilian-group-tier-subtitles.json'
      download_format 'custom-brazilian-subtitles.json'
      download_format 'custom-brazilian-group-tier-dubbed.json'
      download_format 'custom-brazilian-dubbed.json'
      download_format 'custom-original-language.json'
      download_format 'custom-brazilian-group-tier-bad.json'
      download_format 'custom-us-group-tier-premium.json'
      # Plataformas
      download_format 'sonarr-custom-pt-br-globoplay.json'
      download_format 'radarr-custom-pt-br-globoplay.json'
      # Codec
      download_format 'radarr-custom-pt-br-x264.json'
      download_format 'radarr-custom-pt-br-x265.json'
      download_format 'radarr-custom-pt-br-h264.json'
      download_format 'radarr-custom-pt-br-h265.json'
      download_format 'sonarr-custom-pt-br-x264.json'
      download_format 'sonarr-custom-pt-br-x265.json'
      download_format 'sonarr-custom-pt-br-h264.json'
      download_format 'sonarr-custom-pt-br-h265.json'
      # Season Pack
      download_format 'sonarr-custom-season-pack.json'
      # Release Quality - Radarr
      download_format 'radarr-uhd-remux-release.json'
      download_format 'radarr-fhd-remux-release.json'
      download_format 'radarr-hd-remux-release.json'
      download_format 'radarr-uhd-bluray-release.json'
      download_format 'radarr-fhd-bluray-release.json'
      download_format 'radarr-hd-bluray-release.json'
      download_format 'radarr-uhd-web-release.json'
      download_format 'radarr-fhd-web-release.json'
      download_format 'radarr-hd-web-release.json'
      # Release Quality - Sonarr
      download_format 'sonarr-uhd-remux-release.json'
      download_format 'sonarr-fhd-remux-release.json'
      download_format 'sonarr-hd-remux-release.json'
      download_format 'sonarr-uhd-bluray-release.json'
      download_format 'sonarr-fhd-bluray-release.json'
      download_format 'sonarr-hd-bluray-release.json'
      download_format 'sonarr-uhd-web-release.json'
      download_format 'sonarr-fhd-web-release.json'
      download_format 'sonarr-hd-web-release.json'
      
      echo '✅ Custom formats baixados com sucesso!'
      "
    volumes:
      - custom-formats:/config
    restart: "no"
  
  # Configarr
  configarr:
    image: ghcr.io/raydak-labs/configarr:latest
    container_name: configarr
    depends_on:
      download-formats:
        condition: service_completed_successfully
    volumes:
      - ./config/config.yml:/app/config/config.yml:ro
      - ./secrets/secrets.yml:/app/config/secrets.yml:ro
      - custom-formats:/config:ro
      - app-data:/app/repos
    environment:
      - LOG_STACKTRACE=true
      - OTEL_LOG_LEVEL=debug
    network_mode: bridge
    labels:
      ofelia.enabled: "true"
      ofelia.job-exec.configarr-sync.schedule: "0 2 * * *"
      ofelia.job-exec.configarr-sync.command: "/app/configarr"
  
  # Scheduler Ofelia
  ofelia:
    image: mcuadros/ofelia:latest
    container_name: ofelia-scheduler
    depends_on:
      - configarr
    command: daemon --docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

volumes:
  custom-formats:
  app-data:
```

### 5. Executar

```bash
# Execução manual (uma vez)
docker-compose up configarr

# Com scheduler (agendado - modo daemon)
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f configarr

# Forçar execução manual do job agendado
docker exec configarr /app/configarr

# Atualizar custom formats e reiniciar
./download-custom-formats.sh
docker-compose restart configarr
```

---

## ☸️ Kubernetes

### 1. Estrutura de Secrets

Obs: já há um IAC pronto e podendo ser aplicado com kustomize no diretório iac/k8s/configarr, basta alterar os valores dos secrets no arquivo:
- configarr-secrets.yaml
Defina o namespace no arquivo:
- kustomization.yaml

Crie um arquivo `secrets.yml` com suas credenciais:

```yaml
SONARR_URL: "http://sonarr.NAMESPACE.svc.cluster.local:8989"
RADARR_URL: "http://radarr.NAMESPACE.svc.cluster.local:7878"
SONARR_ANIMES_URL: "http://sonarr-animes.NAMESPACE.svc.cluster.local:8990"
RADARR_ANIMES_URL: "http://radarr-animes.NAMESPACE.svc.cluster.local:7879"

SONARR_API_KEY: "sua-api-key-aqui"
RADARR_API_KEY: "sua-api-key-aqui"
SONARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
RADARR_ANIMES_API_KEY: "sua-api-key-animes-aqui"
```

> **Nota:** Substitua `NAMESPACE` pelo namespace real do seu cluster.

### 2. Aplicar Recursos

```bash
# Criar namespace (se necessário)
kubectl create namespace media

# Crie a partir das configuraõesque deseja, Baixa o Config.yaml de acordo O Profile Desejado
#Criar Configmap a partir do config.yml 
kubectl create configmap configarr-config \
  --from-file=config.yml \
  -n media

# Criar Secret a partir do arquivo
kubectl create secret generic configarr-secrets \
  --from-literal=secrets_yml="$(cat secrets.yml)" \
  -n media
```

### 3. CronJob Kubernetes

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: configarr-sync
  namespace: media
spec:
  schedule: "0 2 * * *"  # Todo dia às 2h da manhã
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        metadata:
          labels:
            app: configarr
        spec:
          restartPolicy: Never
          
          # Init Container: Download dos Custom Formats
          initContainers:
            - name: download-custom-formats
              image: curlimages/curl:latest
              command:
                - sh
                - -c
                - |
                  set -e
                  echo "📥 Baixando custom formats do GitHub..."
                  mkdir -p /config/custom_formats
                  
                  BASE_URL="https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download"

                  download_format() {
                    local file=$1
                    echo "  → Baixando: $file"
                    curl -fsSL --retry 3 --retry-delay 2 "$BASE_URL/$file" \
                      -o "/config/custom_formats/$file" || {
                      echo "❌ Erro ao baixar $file"
                      return 1
                    }
                  }

                  # Idioma PT-BR
                  download_format 'custom-brazilian-group-tier-dual-audio.json'
                  download_format 'custom-brazilian-dual-language.json'
                  download_format 'custom-brazilian-group-tier-subtitles.json'
                  download_format 'custom-brazilian-subtitles.json'
                  download_format 'custom-brazilian-group-tier-dubbed.json'
                  download_format 'custom-brazilian-dubbed.json'
                  download_format 'custom-original-language.json'
                  download_format 'custom-brazilian-group-tier-bad.json'
                  download_format 'custom-us-group-tier-premium.json'
                  # Plataformas
                  download_format 'sonarr-custom-pt-br-globoplay.json'
                  download_format 'radarr-custom-pt-br-globoplay.json'
                  # Codec
                  download_format 'radarr-custom-pt-br-x264.json'
                  download_format 'radarr-custom-pt-br-x265.json'
                  download_format 'radarr-custom-pt-br-h264.json'
                  download_format 'radarr-custom-pt-br-h265.json'
                  download_format 'sonarr-custom-pt-br-x264.json'
                  download_format 'sonarr-custom-pt-br-x265.json'
                  download_format 'sonarr-custom-pt-br-h264.json'
                  download_format 'sonarr-custom-pt-br-h265.json'
                  # Season Pack
                  download_format 'sonarr-custom-season-pack.json'
                  # Release Quality - Radarr
                  download_format 'radarr-uhd-remux-release.json'
                  download_format 'radarr-fhd-remux-release.json'
                  download_format 'radarr-hd-remux-release.json'
                  download_format 'radarr-uhd-bluray-release.json'
                  download_format 'radarr-fhd-bluray-release.json'
                  download_format 'radarr-hd-bluray-release.json'
                  download_format 'radarr-uhd-web-release.json'
                  download_format 'radarr-fhd-web-release.json'
                  download_format 'radarr-hd-web-release.json'
                  # Release Quality - Sonarr
                  download_format 'sonarr-uhd-remux-release.json'
                  download_format 'sonarr-fhd-remux-release.json'
                  download_format 'sonarr-hd-remux-release.json'
                  download_format 'sonarr-uhd-bluray-release.json'
                  download_format 'sonarr-fhd-bluray-release.json'
                  download_format 'sonarr-hd-bluray-release.json'
                  download_format 'sonarr-uhd-web-release.json'
                  download_format 'sonarr-fhd-web-release.json'
                  download_format 'sonarr-hd-web-release.json'
                  
                  echo "✅ Todos os custom formats foram baixados!"
                  ls -lah /config/custom_formats/
              
              volumeMounts:
                - name: custom-formats-storage
                  mountPath: /config
          
          # Container Principal: Configarr
          containers:
            - name: configarr
              image: ghcr.io/raydak-labs/configarr:latest
              imagePullPolicy: Always
              env:
                - name: LOG_STACKTRACE
                  value: "true"
                - name: OTEL_LOG_LEVEL
                  value: "info"
              
              volumeMounts:
                - name: configarr-config
                  mountPath: /app/config/config.yml
                  subPath: config.yml
                  readOnly: true
                - name: secrets
                  mountPath: /app/config/secrets.yml
                  subPath: secrets_yml
                  readOnly: true
                - name: custom-formats-storage
                  mountPath: /config
                  readOnly: true
              
              resources:
                requests:
                  memory: "128Mi"
                  cpu: "100m"
                limits:
                  memory: "512Mi"
                  cpu: "500m"
          
          # Volumes
          volumes:
            - name: custom-formats-storage
              emptyDir: {}
            - name: configarr-config
              configMap:
                name: configarr-config
            - name: secrets
              secret:
                secretName: configarr-secrets
```

### 4. Aplicar e Testar

```bash
# Aplicar o CronJob
kubectl apply -f configarr-cronjob.yaml

# Testar execução manual
kubectl create job --from=cronjob/configarr-sync configarr-test -n media

# Acompanhar logs em tempo real
kubectl logs -f job/configarr-test -n media

# Ver todos os logs do job
kubectl logs job/configarr-test -n media --all-containers=true

# Ver status do CronJob
kubectl get cronjob configarr-sync -n media

# Ver histórico de execuções
kubectl get jobs -n media | grep configarr

# Deletar job de teste
kubectl delete job configarr-test -n media
```

---

---

## 🔄 Atualizações Automáticas

### Docker Compose (Ofelia)

Configure a frequência de sincronização editando a label no `docker-compose.yml`:

```yaml
labels:
  ofelia.enabled: "true"
  # Escolha uma das opções abaixo:
  
  # Todo dia às 2h da manhã
  ofelia.job-exec.configarr-sync.schedule: "0 2 * * *"
  
  # A cada 6 horas
  # ofelia.job-exec.configarr-sync.schedule: "0 */6 * * *"
  
  # Toda semana no domingo às 14h
  # ofelia.job-exec.configarr-sync.schedule: "0 14 * * 0"
  
  # A cada 12 horas
  # ofelia.job-exec.configarr-sync.schedule: "0 */12 * * *"
```

### Kubernetes (CronJob)

Edite o campo `schedule` no CronJob:

```yaml
spec:
  # Escolha uma das opções:
  
  schedule: "0 2 * * *"      # Todo dia às 2h
  # schedule: "0 */6 * * *"    # A cada 6 horas
  # schedule: "0 14 * * 0"     # Toda semana no domingo às 14h
  # schedule: "*/30 * * * *"   # A cada 30 minutos (não recomendado)
```

> **Dica:** Use [crontab.guru](https://crontab.guru/) para testar expressões cron.

---

## 📦 Releases e Versionamento

### Branch Strategy

| Branch | Finalidade | Downloads |
|--------|-----------|-----------|
| **alpha** | Desenvolvimento ativo | Testes internos |
| **beta** | Validação | `latest` release |
| **stable** | Produção | Releases versionadas (v1.0.0) |

> **Nota:** As branches `develop` e `main` permanecem intactas para compatibilidade com downloads existentes.

### Como Baixar

**Custom Formats (sempre a versão mais recente):**
```
https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download/NOME-DO-ARQUIVO.json
```

**Configs versionados:**
```
https://github.com/marcosviniciusi/trash-guides-ptbr/releases/download/v1.0.0/config-DUBLADO-4K-HDR.yaml
```

### Criando uma Release

Releases são criadas automaticamente via GitHub Actions:

1. **Via tag:** `git tag v1.0.0 && git push origin v1.0.0`
2. **Via GitHub UI:** Actions > Release > Run workflow (informar versao e branch)

Cada release inclui:
- Todos os custom formats JSON como assets individuais
- Todos os configs YAML como assets individuais
- ZIPs: `custom-formats.zip`, `configarr-configs.zip`, `trash-guides-ptbr-completo.zip`
- Docker compose files renomeados (`docker-compose-manual.yaml`, `docker-compose-automatico.yaml`)
- Script `download-custom-formats.sh`

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Seja adicionando novos custom formats, melhorando a documentação ou reportando bugs.

### Como Contribuir

1. **Fork** este repositório
2. Crie um **branch** para sua feature (`git checkout -b feature/novo-formato`)
3. Adicione o custom format na pasta `custom-formats/`
4. **Teste** com Radarr/Sonarr em ambiente real
5. Atualize este **README.md** com as informações do novo formato
6. **Commit** suas mudanças (`git commit -am 'Adiciona formato XYZ para releases 4K'`)
7. **Push** para o branch (`git push origin feature/novo-formato`)
8. Abra um **Pull Request** detalhando suas mudanças

### Diretrizes de Custom Formats

- Use regex precisos e testados
- Documente o propósito e comportamento esperado
- Inclua exemplos de nomes de release que devem/não devem corresponder
- Teste com pelo menos 10 releases reais antes de submeter

---

## ❓ FAQ

**P: Esses formatos substituem os TRaSH Guides oficiais?**  
R: Não! Eles são **complementares**. Os TRaSH Guides cobrem qualidade geral (codecs, HDR, áudio), enquanto estes formatos focam em conteúdo PT-BR. Use ambos juntos para melhores resultados.

**P: Preciso usar todos os custom formats disponíveis?**  
R: Não. Escolha apenas os que fazem sentido para seu caso de uso. Por exemplo, se você não assiste animes, pode ignorar os formatos de anime.

**P: Porque houve alteração da estrutura?**  
R: Pensando a longo prazo e organização e suporte a legendas e dublados, foram realizadas alteração na estrutura de diretórios para cobrir todos os tipos de midias.

**P: Como atualizo os custom formats?**  
R: Se estiver usando Configarr com agendamento (Ofelia ou CronJob), a atualização é automática. Para atualização manual, execute `./download-custom-formats.sh` e `docker-compose restart configarr`.

**P: Posso usar sem Docker/Kubernetes?**  
R: Sim! Você pode instalar o Configarr localmente seguindo a [documentação oficial](https://github.com/raydak-labs/configarr) ou adicionar os custom formats manualmente pela interface web.

**P: Os scores sugeridos são obrigatórios?**  
R: Não, são apenas recomendações baseadas em testes. Ajuste conforme suas preferências pessoais e prioridades.

**P: Como funciona o Ofelia?**  
R: Ofelia é um scheduler de jobs para Docker similar ao cron. Ele monitora containers com labels específicas e executa comandos baseado em agendamentos cron, sem necessidade de crontab do host.

**P: Por que os scores de anime são tão altos?**  
R: Para garantir que releases com PT-BR sempre tenham prioridade absoluta sobre qualquer outra consideração de qualidade. Animes DUAL AUDIO/LEGENDADOS/DUBLADOS em PT-BR são raros, então priorizamos sua captura.

**P: Porque há grupos de Releases pt-BR como Ruins?**  
R: Alguns grupos de lançamento são amplamente conhecidos por apresentarem materiais de baixa qualidade ou práticas desonestas, como a retag, onde renomeiam os arquivos de forma enganosa para parecerem de uma qualidade superior à real. Esses grupos não têm permissão para realizar envios em alguns tracker pt-br privados, e há razões claras para isso. decisão é manter o projeto com mesmas praticas destes trackers.
Entre as práticas comuns desses grupos estão a inserção de propagandas indesejadas no arquivo de media info, envio de BD Autorado, envio de versões com nomenclatura falsa, como rotular um arquivo como REMUX quando, na verdade, é apenas um encode de qualidade inferior. Outros exemplos incluem classificar arquivos WEBRip como WEB-DL para dar a impressão de uma fonte mais refinada, além de outros envios que fogem completamente dos padrões estabelecidos, como arquivos com marca d'água, legendas com propagandas, upscaling artificial que deteriora a qualidade, e spam de links ou materiais.
Caso queira baixa-los, basta remover do Config.yaml e também do scripts para baixa-lo. fica a critério, em animes, muitas vezes devido a dificuldade de encontrar fontes com conteúdo pt-Br, deixei uma penalização mais branda e com custom stoe positivo, mas se quiser aumentar a penalização, basta alterar para -100000.

**P: Posso usar em produção?**  
R: Sim! O Configarr e estes custom formats são usados por muitos usuários em produção. Recomendamos testar primeiro em um ambiente de staging.

**P: Como reporto problemas ou sugiro melhorias?**  
R: Abra uma [issue no GitHub](https://github.com/marcosviniciusi/trash-guides-ptbr/issues) com detalhes do problema ou sugestão. Exemplos de releases que não funcionaram como esperado são muito úteis!

---

## 🙏 Créditos

- Baseado no trabalho excepcional do [TRaSH Guides](https://trash-guides.info/)
- Desenvolvido com ❤️ para a comunidade brasileira de *arr apps
- Agradecimento especial a todos os [contribuidores](https://github.com/marcosviniciusi/trash-guides-ptbr/graphs/contributors)

---

**💬 Dúvidas ou sugestões?** 

- [Abra uma issue](https://github.com/marcosviniciusi/trash-guides-ptbr/issues) para reportar problemas
- [Contribua com um pull request](https://github.com/marcosviniciusi/trash-guides-ptbr/pulls) para melhorias

---

<div align="center">

**Feito com ❤️ para a comunidade brasileira de homelabs**

[⬆ Voltar ao topo](#trash-guides-pt-br---custom-formats)

</div>