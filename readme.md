# TRaSH Guides PT-BR - Custom Formats

Custom Formats em Português Brasileiro para Radarr e Sonarr, otimizados para conteúdo nacional com (DUAL-AUDIO)/legendas PT-BR.

[![Configarr Compatible](https://img.shields.io/badge/Configarr-Compatible-green)](https://github.com/raydak-labs/configarr)
[![Radarr Compatible](https://img.shields.io/badge/Radarr-Compatible-green)](https://github.com/Radarr/Radarr)
[![Sonarr Compatible](https://img.shields.io/badge/Sonarr-Compatible-green)](https://github.com/Sonarr/Sonarr)
[![TRaSH-Guides Compatible](https://img.shields.io/badge/TRaSHGuides-Compatible-green)](https://github.com/TRaSH-Guides/Guides)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Índice

- [Sobre](#-sobre)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Custom Formats Disponíveis](#-custom-formats-disponíveis)
  - [Radarr (Filmes)](#-radarr-filmes)
  - [Radarr (Animes)](#animes-radarr)
  - [Sonarr (Séries)](#-sonarr-séries)
  - [Sonarr (Animes)](#animes-sonarr)
- [Configurando os Quality Profiles](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#-configurando-os-quality-profiles)
  - [Criando o Profile "HD"](#criando-o-profile-com-nome-hd)
- [Configurando Manualmente os custom Formats](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#configurando-manualmente-os-custom-formats)
- [O que é o Configarr?](#-o-que-é-o-configarr)
  - [Vantagens](#vantagens)
  - [Como Funciona?](#como-funciona)
  - [Principais Benefícios](#-principais-benefícios)
  - [Como Configurar?](#como-configura-lo)
    - [Pré-Requisitos](#pré-requisitos)
    - [Docker Compose - Execução Manual](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#docker-compose---execu%C3%A7%C3%A3o-manual)
    - [Docker Compose - Execução Automatica](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#docker-compose---execu%C3%A7%C3%A3o-agendada-com-ofelia)
    - [Kubernetes](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#%EF%B8%8F-kubernetes)
- [Estrutura de Scores](#-estrutura-de-scores)
- [Atualizações Automáticas](#-atualizações-automáticas)
- [Contribuindo](#-contribuindo)
- [FAQ](#-faq)

## 🎯 Sobre

Este repositório contém **Custom Formats personalizados** desenvolvidos especificamente para a comunidade brasileira, priorizando:

- ✅ **Conteúdo em PT-BR**: Releases DUAL Audio/legendados em português brasileiro
- ✅ **Grupos confiáveis**: Releases de grupos brasileiros e portugueses reconhecidos
- ✅ **Qualidade otimizada**: Filtros específicos para garantir qualidade adequada
- ✅ **Foco em animes**: Formatos especializados para conteúdo japonês com PT-BR
- ✅ **Automação completa**: Compatível com Configarr para sincronização automática

> **Nota importante:** Estes formatos são **complementares** aos [TRaSH Guides oficiais](https://trash-guides.info/), não substitutos. Use ambos para obter os melhores resultados!

## 📁 Estrutura do Repositório

```
trash-guides-ptbr/
├── README.md
├── configarr/
│   ├── config.yaml                                    # Configuração completa SEM HDR
│   └── config-HDR-ON.yaml                             # Configuração completa COM HDR
├── custom-formats/                                    # Todos os custom formats
│   ├── custom-web-tier-ptbr-dual.json                 # DUAL-AUDIO (Global)
│   ├── custom-web-tier-ptbr-not-dual.json             # Legendado PT-BR (Global)
│   ├── custom-web-tier-ptbr-not-group-radarr.json     # Legendado PT-BR não mapeados (Radarr)
│   ├── custom-web-tier-ptbr-not-group-sonarr.json     # Legendado PT-BR não mapeados (Sonarr)
│   ├── custom-animes-not-brazilian-radarr.json        # Penaliza animes sem PT-BR (Radarr)
│   ├── custom-animes-not-brazilian-sonarr.json        # Penaliza animes sem PT-BR (Sonarr)
│   ├── custom-animes-not-original-radarr.json         # Penaliza áudio não original (Radarr)
│   ├── custom-animes-not-original-sonarr.json         # Penaliza áudio não original (Sonarr)
│   ├── custom-animes-not-portuguese-radarr.json       # Penaliza sem português (Radarr)
│   ├── custom-animes-not-portuguese-sonarr.json       # Penaliza sem português (Sonarr)
│   ├── custom-animes-toonshub-pt-radarr.json          # Legendado ToonsHub PT-PT (Radarr)
│   ├── custom-animes-toonshub-pt-sonarr.json          # Legendado ToonsHub PT-PT (Sonarr)
│   ├── custom-animes-toonshub-ptbr-radarr.json        # Legendado Legendado ToonsHub PT-BR (Radarr)
│   ├── custom-animes-toonshub-ptbr-sonarr.json        # Legendado ToonsHub PT-BR (Sonarr)
│   └── custom-bad-pt-br-groups.json                   # Grupos PT-Br Banidos
└── iac/                                               # Infraestrutura como Código
    ├── docker-compose/ 
    │   ├── automatico/                                
    │   │   └── docker-compose.yaml                    # Docker Compose Automatico
    │   └── manual/
    │       ├── docker-compose.yaml                    # Docker Compose Manual
    │       └── download-custom-formats.sh             # Bash Downloads Custom Profiles
    └── k8s/    
        └── configarr/                                 # Manifestos Kubernetes
            ├── configarr-config.yaml
            ├── configarr-cronjob.yaml
            ├── configarr-pvc.yaml
            ├── configarr-secrets.yaml
            └── kustomization.yaml
```

## 📦 Custom Formats Disponíveis

### 🎬 Radarr (Filmes)

#### Web Tier PT-BR

| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) de grupos confiáveis | +6000 |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado) | +5500 |
| **custom-web-tier-ptbr-not-group-radarr** | Prioriza releases PT-BR não mapeados (legendado) | +5000 |
| **custom-bad-pt-br-groups.jsonl** | Grupos pt-BR Banidos | -10000 |

#### Animes (Radarr)

| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) de grupos confiáveis | +60000000 |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado) | +55000000 |
| **custom-web-tier-ptbr-not-group-radarr** | Prioriza releases PT-BR não mapeados (legendado) | +50000000 |
| **custom-animes-toonshub-ptbr-radarr** | Prioriza releases ToonsHub PT-BR (legendado) | +750000 |
| **custom-animes-toonshub-pt-radarr** | Prioriza releases ToonsHub PT-PT (legendado) | +700000 |
| **custom-animes-not-brazilian-radarr** | Penaliza releases sem PT-BR | -100000 |
| **custom-animes-not-original-radarr** | Penaliza áudio não original | -100000 |
| **custom-animes-not-portuguese-radarr** | Penaliza conteúdo sem português | -100000 |
| **custom-bad-pt-br-groups.jsonl** | Grupos pt-BR Banidos | -10000 |

### 📺 Sonarr (Séries)

#### Web Tier PT-BR

| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) | +7000 |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado) | +6500 |
| **custom-web-tier-ptbr-not-group-sonarr** | Prioriza releases PT-BR não mapeados (legendado) | +6000 |
| **custom-bad-pt-br-groups.jsonl** | Grupos pt-BR Banidos | -10000 |

#### Animes (Sonarr)

| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) | +60000000 |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado) | +55000000 |
| **custom-web-tier-ptbr-not-group-sonarr** | Prioriza releases PT-BR não mapeados (legendado) | +50000000 |
| **custom-animes-toonshub-ptbr-sonarr** | Prioriza ToonsHub PT-BR (legendado) | +750000 |
| **custom-animes-toonshub-pt-sonarr** | Prioriza ToonsHub PT-PT (legendado) | +700000 |
| **custom-animes-not-brazilian-sonarr** | Penaliza releases sem PT-BR | -10000 |
| **custom-animes-not-original-sonarr** | Penaliza áudio não original | -10000 |
| **custom-animes-not-portuguese-sonarr** | Penaliza sem português | -10000 |
| **custom-bad-pt-br-groups.jsonl** | Grupos pt-BR Banidos | +10000 |

## 🔧 Configurando os Quality Profiles

### Pré-requisito: Criar Quality Profile "HD"

Antes de configurar os custom formats, você precisa ter um Quality Profile chamado **"HD"** (ou ajustar o nome no `config.yml`).

### Criando o Profile com Nome "HD"

#### No Radarr/Sonarr:

1. Acesse **Settings → Profiles**
2. Clique em **+** para adicionar novo perfil
3. Configure:
   - **Name**: `HD`
   - **Upgrades Allowed**: ✅ (habilitado)
   - **Upgrade Until**: Selecione a qualidade máxima desejada (ex: Bluray-1080p)
   - **Qualities**: Selecione as qualidades desejadas (recomendado: WEBDL-1080p, WEBRip-1080p, Bluray-1080p, Remux-1080p)
   - **Minimum Custom Format Score**: `0` (ou deixe em branco)
4. Clique em **Save**
5. **Opcional Altamente Recomendavel:** Configuração de esquemas de nomes dos arquivos [Sonarr](https://trash-guides.info/Sonarr/Sonarr-recommended-naming-scheme/#recommended-naming-scheme) e [Radarr](https://trash-guides.info/Radarr/Radarr-recommended-naming-scheme/#recommended-naming-scheme) 
  - [Sonarr Series](https://trash-guides.info/Sonarr/Sonarr-recommended-naming-scheme/#standard)
```
{Series TitleYear} - S{season:00}E{episode:00} - {Episode CleanTitle:90} {[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```
 - [Radarr Filmes](https://trash-guides.info/Radarr/Radarr-recommended-naming-scheme/#standard-movie-format)
```
{Movie CleanTitle} {(Release Year)} - {{Edition Tags}} {[MediaInfo 3D]}{[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```
  - [Sonarr Animes](https://trash-guides.info/Sonarr/Sonarr-recommended-naming-scheme/#anime)
```
{Series TitleYear} - S{season:00}E{episode:00} - {absolute:000} - {Episode CleanTitle:90} {[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{MediaInfo AudioLanguages}{[MediaInfo VideoDynamicRangeType]}[{Mediainfo VideoCodec }{MediaInfo VideoBitDepth}bit]{-Release Group}
```
  - [Radarr Animes](https://trash-guides.info/Radarr/Radarr-recommended-naming-scheme/#standard-movie-format)
```
{Movie CleanTitle} {(Release Year)} - {{Edition Tags}} {[MediaInfo 3D]}{[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```
## Configurando Manualmente os custom Formats
## obs: siga apenas este passo se não deseja o uso do configarr.
#### No Radarr/Sonarr:

1. Acesse **Settings → Custom Formats**
2. Clique em **+** para adicionar novo formato
3. Cole o conteúdo do JSON desejado (disponível na pasta `custom-formats/`)
4. Salve e configure o score no Quality Profile correspondente

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
            score: 6000
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
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/iac/docker-compose/manual/docker-compose.yaml -o docker-compose.yaml
```
Obs: Ja efetua o download do docker compose. e também ja tem criado o script para baixar os custom formats, caso queira baixa-lo, use este script abaixo:

```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/iac/docker-compose/manual/docker-compose.yaml -o docker-compose.yaml
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/iac/docker-compose/manual/download-custom-formats.sh -o download-custom-formats.sh
chmod +x download-custom-formats.sh
./download-custom-formats.sh
```
Obs 2: Se seguir o este segundo script, Siga os passos 2 e 3, poderá ir direto a esta [Passo de execuçãp](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#5-executar).

### 2. Criar secrets.yml

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

> **Dica:** Substitua `sonarr`, `radarr`, etc. pelos nomes reais dos seus containers/serviços.
### 3. Baixar config.yml com todos Custom Formats do trashguide e Scores

```bash
# Opção 1: Baixar diretamente do repositório
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/configarr/config.yaml \
  -o config/config.yml

# Opção 2: Para configuração COM HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/configarr/config-HDR-ON.yaml \
  -o config/config.yml
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
            score: 6000

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
            score: 7000

# [Veja config.yml completo no repositório]
```

### 4. Script de Download dos Custom Formats

```bash
cat > download-custom-formats.sh << 'EOF'
#!/bin/bash

BASE_URL="https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats"

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

# Custom Formats Globais
download_format "custom-web-tier-ptbr-dual.json"
download_format "custom-web-tier-ptbr-not-dual.json"

# Radarr
download_format "custom-web-tier-ptbr-not-group-radarr.json"
download_format "custom-animes-not-brazilian-radarr.json"
download_format "custom-animes-not-original-radarr.json"
download_format "custom-animes-not-portuguese-radarr.json"
download_format "custom-animes-toonshub-pt-radarr.json"
download_format "custom-animes-toonshub-ptbr-radarr.json"

# Sonarr
download_format "custom-web-tier-ptbr-not-group-sonarr.json"
download_format "custom-animes-not-brazilian-sonarr.json"
download_format "custom-animes-not-original-sonarr.json"
download_format "custom-animes-not-portuguese-sonarr.json"
download_format "custom-animes-toonshub-pt-sonarr.json"
download_format "custom-animes-toonshub-ptbr-sonarr.json"
# Bad pt-Br Groups
download_format "custom-bad-pt-br-groups.json"

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
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/iac/docker-compose/automatico/docker-compose.yaml -o docker-compose.yaml
```
Obs: Ja efetua o download do arquivo docker-compose.yaml, siga os passos 2 e 3, poderá ir direto a esta [Passo de execuçãp](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#5-executar).
### 2. Criar secrets.yml

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

> **Dica:** Substitua `sonarr`, `radarr`, etc. pelos nomes reais dos seus containers/serviços.
### 3. Baixar config.yml com todos Custom Formats do trashguide e Scores

```bash
# Opção 1: Baixar diretamente do repositório
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/configarr/config.yaml \
  -o config/config.yml

# Opção 2: Para configuração COM HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/configarr/config-HDR-ON.yaml \
  -o config/config.yml
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
            score: 6000

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
            score: 7000

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
      echo '📥 Baixando custom formats...' &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-web-tier-ptbr-dual.json -o /config/custom_formats/custom-web-tier-ptbr-dual.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-web-tier-ptbr-not-dual.json -o /config/custom_formats/custom-web-tier-ptbr-not-dual.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-web-tier-ptbr-not-group-radarr.json -o /config/custom_formats/custom-web-tier-ptbr-not-group-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-web-tier-ptbr-not-group-sonarr.json -o /config/custom_formats/custom-web-tier-ptbr-not-group-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-brazilian-sonarr.json -o /config/custom_formats/custom-animes-not-brazilian-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-original-sonarr.json -o /config/custom_formats/custom-animes-not-original-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-portuguese-sonarr.json -o /config/custom_formats/custom-animes-not-portuguese-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-toonshub-pt-sonarr.json -o /config/custom_formats/custom-animes-toonshub-pt-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-toonshub-ptbr-sonarr.json -o /config/custom_formats/custom-animes-toonshub-ptbr-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-brazilian-radarr.json -o /config/custom_formats/custom-animes-not-brazilian-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-original-radarr.json -o /config/custom_formats/custom-animes-not-original-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-not-portuguese-radarr.json -o /config/custom_formats/custom-animes-not-portuguese-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-toonshub-pt-radarr.json -o /config/custom_formats/custom-animes-toonshub-pt-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-animes-toonshub-ptbr-radarr.json -o /config/custom_formats/custom-animes-toonshub-ptbr-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats/custom-bad-pt-br-groups.json -o /config/custom_formats/custom-bad-pt-br-groups.json
      echo '✅ Custom formats baixados com sucesso!'
      "
    volumes:
      - custom-formats:/config/custom-formats
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
      - custom-formats:/config/custom-formats:ro
      - app-data:/app/repos
    environment:
      - LOG_STACKTRACE=true
      - OTEL_LOG_LEVEL=debug
    network_mode: bridge
    labels:
      ofelia.enabled: "true"
      ofelia.job-exec.configarr-sync.schedule: "0 2 * * *"  # Todo dia às 2h
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

# Criar ConfigMap com config.yml
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
                  
                  BASE_URL="https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/main/custom-formats"
                  
                  # Função para download com retry
                  download_file() {
                    local file=$1
                    echo "  → Baixando: $file"
                    curl -fsSL --retry 3 --retry-delay 2 "$BASE_URL/$file" \
                      -o "/config/custom_formats/$file" || {
                      echo "❌ Erro ao baixar $file"
                      return 1
                    }
                  }
                  
                  # Download de todos os formatos
                  download_file "custom-web-tier-ptbr-dual.json"
                  download_file "custom-web-tier-ptbr-not-dual.json"
                  download_file "custom-web-tier-ptbr-not-group-radarr.json"
                  download_file "custom-web-tier-ptbr-not-group-sonarr.json"
                  download_file "custom-animes-not-brazilian-sonarr.json"
                  download_file "custom-animes-not-original-sonarr.json"
                  download_file "custom-animes-not-portuguese-sonarr.json"
                  download_file "custom-animes-toonshub-pt-sonarr.json"
                  download_file "custom-animes-toonshub-ptbr-sonarr.json"
                  download_file "custom-animes-not-brazilian-radarr.json"
                  download_file "custom-animes-not-original-radarr.json"
                  download_file "custom-animes-not-portuguese-radarr.json"
                  download_file "custom-animes-toonshub-pt-radarr.json"
                  download_file "custom-animes-toonshub-ptbr-radarr.json"
                  # Bad pt-Br Groups
                  download_file "custom-bad-pt-br-groups.json"
                  
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

## 📊 Estrutura de Scores

### Filmes/Séries (Radarr/Sonarr)

| Categoria | Faixa de Score |
|-----------|----------------|
| **Custom Formats PT-BR** | +5000 a +7000 |
| **Áudio de Alta Qualidade** | +1000 a +5000 |
| **Remux/Bluray Tiers** | +1700 a +1950 |
| **Penalizações** | -10000 a -100000 |

### Animes (Radarr/Sonarr)

| Categoria | Score |
|-----------|-------|
| **Web Tier PT-BR Dual** | +60000000 |
| **Web Tier PT-BR Not Dual** | +55000000 |
| **Web Tier PT-BR not-group** | +50000000 |
| **ToonsHub PT-BR** | +750000 |
| **ToonsHub PT-PT** | +700000 |
| **Penalizações (Sem PT-BR)** | -100000 |

> **Nota:** Os scores para animes são intencionalmente muito altos para garantir prioridade absoluta sobre outros formatos.

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

### Padrão de Nomenclatura

Para manter a consistência do repositório:

- **`custom-web-tier-ptbr-*.json`** - Formatos para web releases PT-BR
- **`custom-animes-*.json`** - Formatos específicos para animes
- **Prefixo `custom-`** - Para diferenciar dos formatos oficiais do TRaSH
- **Sufixo `-radarr` ou `-sonarr`** - Para especificar a aplicação

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

**P: Como atualizo os custom formats?**  
R: Se estiver usando Configarr com agendamento (Ofelia ou CronJob), a atualização é automática. Para atualização manual, execute `./download-custom-formats.sh` e `docker-compose restart configarr`.

**P: Posso usar sem Docker/Kubernetes?**  
R: Sim! Você pode instalar o Configarr localmente seguindo a [documentação oficial](https://github.com/raydak-labs/configarr) ou adicionar os custom formats manualmente pela interface web.

**P: Os scores sugeridos são obrigatórios?**  
R: Não, são apenas recomendações baseadas em testes. Ajuste conforme suas preferências pessoais e prioridades.

**P: Como funciona o Ofelia?**  
R: Ofelia é um scheduler de jobs para Docker similar ao cron. Ele monitora containers com labels específicas e executa comandos baseado em agendamentos cron, sem necessidade de crontab do host.

**P: Por que os scores de anime são tão altos?**  
R: Para garantir que releases com PT-BR sempre tenham prioridade absoluta sobre qualquer outra consideração de qualidade. Animes DUAL AUDIO/legendados em PT-BR são raros, então priorizamos sua captura.

**P: Porque há grupos de Releases pt-BR banidos?**  
R: Alguns grupos de lançamento são amplamente conhecidos por apresentarem materiais de baixa qualidade ou práticas desonestas, como a retag, onde renomeiam os arquivos de forma enganosa para parecerem de uma qualidade superior à real. Esses grupos não têm permissão para realizar envios em alguns tracker pt-br privados, e há razões claras para isso. decisão é manter o projeto com mesmas praticas destes trackers.
Entre as práticas comuns desses grupos estão a inserção de propagandas indesejadas no arquivo de media info, envio de BD Autorado, envio de versões com nomenclatura falsa, como rotular um arquivo como REMUX quando, na verdade, é apenas um encode de qualidade inferior. Outros exemplos incluem classificar arquivos WEBRip como WEB-DL para dar a impressão de uma fonte mais refinada, além de outros envios que fogem completamente dos padrões estabelecidos, como arquivos com marca d'água, legendas com propagandas, upscaling artificial que deteriora a qualidade, e spam de links ou materiais.
Caso queira baixa-los, basta remover do Config.yaml e também do scripts para baixa-lo. fica a critério, em animes, muitas vezes devido a dificuldade de encontrar fontes com conteúdo pt-Br, deixei uma penalização mais branda, mas se quiser aumentar a penalização, basta incrementa-las para -100000.

**P: Posso usar em produção?**  
R: Sim! O Configarr e estes custom formats são usados por muitos usuários em produção. Recomendamos testar primeiro em um ambiente de staging.

**P: Como reporto problemas ou sugiro melhorias?**  
R: Abra uma [issue no GitHub](https://github.com/marcosviniciusi/trash-guides-ptbr/issues) com detalhes do problema ou sugestão. Exemplos de releases que não funcionaram como esperado são muito úteis!

---

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Créditos

- Baseado no trabalho excepcional do [TRaSH Guides](https://trash-guides.info/)
- Desenvolvido com ❤️ para a comunidade brasileira de *arr apps
- Mantido por [Marcos Gabriel](https://github.com/marcosviniciusi)
- Agradecimento especial a todos os [contribuidores](https://github.com/marcosviniciusi/trash-guides-ptbr/graphs/contributors)

---

## 🌟 Apoie o Projeto

Se este projeto foi útil para você, considere:

- ⭐ Dar uma **estrela** no repositório
- 🔄 **Compartilhar** com outros usuários brasileiros de Radarr/Sonarr
- 🐛 **Reportar bugs** ou sugerir melhorias
- 🤝 **Contribuir** com novos custom formats ou melhorias na documentação

---

**💬 Dúvidas ou sugestões?** 

- [Abra uma issue](https://github.com/marcosviniciusi/trash-guides-ptbr/issues) para reportar problemas
- [Contribua com um pull request](https://github.com/marcosviniciusi/trash-guides-ptbr/pulls) para melhorias

---

<div align="center">

**Feito com ❤️ para a comunidade brasileira de homelabs**

[⬆ Voltar ao topo](#trash-guides-pt-br---custom-formats)

</div>