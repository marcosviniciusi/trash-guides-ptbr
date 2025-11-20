# TRaSH Guides PT-BR - Custom Formats

Custom Formats em Português Brasileiro para Radarr e Sonarr, otimizados para conteúdo nacional com (DUAL-AUDIO)/legendas PT-BR e também o Dublado.

[![Configarr Compatible](https://img.shields.io/badge/Configarr-Compatible-green)](https://github.com/raydak-labs/configarr)
[![Radarr Compatible](https://img.shields.io/badge/Radarr-Compatible-green)](https://github.com/Radarr/Radarr)
[![Sonarr Compatible](https://img.shields.io/badge/Sonarr-Compatible-green)](https://github.com/Sonarr/Sonarr)
[![TRaSH-Guides Compatible](https://img.shields.io/badge/TRaSHGuides-Compatible-green)](https://github.com/TRaSH-Guides/Guides)

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
- [Custom Formats Disponíveis](#-custom-formats-disponíveis)
  - [Legendados](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#legendados)
  - [Dublados](https://github.com/marcosviniciusi/trash-guides-ptbr?tab=readme-ov-file#dublados)
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
├── configarr/
│   ├── config-LEGENDADO.yaml                          # Configuração completa LEGENDADO SEM HDR
│   ├── config-LEGENDADO-HDR-ON.yaml                   # Configuração completa LEGENDADO COM HDR
│   ├── config-DUBLADO.yaml                            # Configuração completa  DUBLADO SEM HDR
│   └── config-DUBLADO-HDR-ON.yaml                     # Configuração completa  DUBLADO COM HDR
│   ├── config-LEGENDADO-SEM-ANIMES.yaml               # Configuração SEM ANIMES LEGENDADO SEM HDR
│   ├── config-LEGENDADO-HDR-ON-SEM-ANIMES.yaml        # Configuração SEM ANIMES LEGENDADO COM HDR
│   ├── config-DUBLADO-SEM-ANIMES.yaml                 # Configuração SEM ANIMES  DUBLADO SEM HDR
│   └── config-DUBLADO-HDR-ON-SEM-ANIMES.yaml          # Configuração SEM ANIMES  DUBLADO COM HDR
├── custom-formats/    					                       # Todos os custom formats
│   │   #GLOBAIS                               
│   ├── custom-pt-br-dual-audio.json                   # Brasilian DUAL-AUDIO (Verifica se corresponde na busca dos index)
│   ├── custom-pt-br-dual-language.json                # Brasilian DUAL-AUDIO ( Tag para Importação Verifiando o Audio)
│   ├── custom-pt-br-dublado-language.json             # Lingua Portuguesa ( Tag para Importação Verifiando o Audio)
│   ├── custom-pt-br-dublado.json                      # Regex paa Releases Dublados
│   ├── custom-pt-br-legendado.json                    # Regex para Releases Legendados
│   ├── custom-pt-br-original-language.json            # Lingua Original ( Tag para Importação Verifiando o Audio)
│   ├── custom-pt-br-web-tier-bad-group.json           # Grupos Não Confiaveis
│   └── custom-pt-br-web-tier.json                     # Releases Groups PT-BR
├── iac/                                               # Infraestrutura como Código
│   ├── docker-compose/ 
│   │   ├── automatico/                                
│   │   │   └── docker-compose.yaml                    # Docker Compose Automatico
│   │   └── manual/
│   │       ├── docker-compose.yaml                    # Docker Compose Manual
│   │       └── download-custom-formats.sh             # Bash Downloads Custom Profiles
│   └── k8s/    
│       └── configarr/                                 # Manifestos Kubernetes
│           ├── configarr-config.yaml
│           ├── configarr-cronjob.yaml
│           ├── configarr-pvc.yaml
│           ├── configarr-secrets.yaml
│           └── kustomization.yaml
└── prowlarr-indexes/                                  # Indexes do Prowlarr Modificados 
                                                       #( Adicionar dentro do container do Prowlarr no /config/Definition/Custom)

```

# 📦 Custom Formats Disponíveis

## 🎬 Perfis
## LEGENDADOS
------------------------------------------------------------------
### 📺 Radarr/Sonarr (GLOBAL)

#### Web Tier PT-BR

| Custom Format | Descrição | Score Recomendado Series/Movies| Score Recomendado Animes |
|---------------|-----------|-------------------|----------------------------------------------|
| **custom-pt-br-dual-audio** | Prioriza Releases com Titulos - BRAZILIAN-DUAL-AUDIO/NACIONAL | +10000 | +30000000 |
| **custom-pt-br-dual-languageg** | Tag Para BRAZILIAN-DUAL-AUDIO PÓS IMPORTAÇÃO | +10000 | +30000000 |
| **custom-pt-br-legendado** | Prioriza Releases COM REGEX LEGENDADOS e afins... | +7500 | +25000000 |
| **custom-pt-br-original-language** | Tag Para Language Original PÓS IMPORTAÇÃO | +8000 | +1000 |
| **custom-pt-br-web-tier-bad-group** | Grupos pt-BR não Confiaveis | +7000 | +800000 |
| **custom-pt-br-web-tier** | Grupos pt-BR Confiaveis | +300 | +30000000 |

## DUBLADOS
------------------------------------------------------------------
### 📺 Radarr/Sonarr (GLOBAL)

#### Web Tier PT-BR

| Custom Format | Descrição | Score Recomendado Series/Movies| Score Recomendado Animes |
|---------------|-----------|-------------------|----------------------------------------------|
| **custom-pt-br-dual-audio** | Prioriza Releases com Titulos - BRAZILIAN-DUAL-AUDIO/NACIONAL | +10000 | +30000000 |
| **custom-pt-br-dual-languageg** | Tag Para BRAZILIAN-DUAL-AUDIO PÓS IMPORTAÇÃO | +10000 | +30000000 |
| **custom-pt-br-dublado** | Prioriza Releases COM REGEX Dublados e afins... | +7500 | +25000000 |
| **custom-pt-br-dublado-language** | Tag Para Language Portugues PÓS IMPORTAÇÃO | +8000 | +1000 |
| **custom-pt-br-web-tier-bad-group** | Grupos pt-BR não Confiaveis | +7000 | +800000 |
| **custom-pt-br-web-tier** | Grupos pt-BR Confiaveis | +300 | +30000000 |


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
   - **Upgrade Until**: Selecione a qualidade máxima desejada (Ex: Bluray-1080p)
   - **Qualities**: Selecione as qualidades desejadas (Ex: WEBDL-1080p, WEBRip-1080p, Bluray-1080p, Remux-1080p)
   - **Minimum Custom Format Score** Recomendado:
      - **Filmes/Series Mix de Conteudos Gringos mas que prefira PT-BR: 250 ( caso tenha um Bazarr configurado)
      - **Filmes/Series Apenas Dual Audio/Legendados: 7500 
      - **Filmes/Series Apenas Dual Audio/Dublado: 7500
      - **Animes GLOBAL Apenas Dual Audio/Legendado/Dublados: 200000
   - **Upgrade Until Custom Format Score** Recomendado:
      - **Filmes/Series Sem HDR: 25000
      - **Filmes/Series Com HDR: 26500
      - **Animes : 60000000
4. Clique em **Save**
5. **Pré Requisitos OBRIGATÓRIO:** Configuração de esquemas de nomes dos arquivos [Sonarr](https://trash-guides.info/Sonarr/Sonarr-recommended-naming-scheme/#recommended-naming-scheme) e [Radarr](https://trash-guides.info/Radarr/Radarr-recommended-naming-scheme/#recommended-naming-scheme) - Sem Estas Configurações, no momento do Import, ocorrerá erros ao importar.
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
## Prowlarr Custom Indexers - Brazilian Trackers
Indexers customizados para trackers brasileiros otimizados para Radarr/Sonarr com padronização de títulos.
## Propósito
A comunidade brasileira de trackers faz um **trabalho excepcional** disponibilizando conteúdo de qualidade em português. No entanto, cada tracker segue sua própria convenção de nomenclatura, o que é perfeitamente compreensível dada a diversidade e autonomia de cada comunidade.

Estes indexers foram desenvolvidos para criar uma **camada de padronização** que unifica os títulos dos releases brasileiros em diversos trackers, tanto públicos quanto privados, **sem alterar o excelente trabalho já realizado pelas comunidades**.

Com esta padronização, você terá:
- ✅ **Resultados consistentes** entre diferentes trackers
- ✅ **Custom Formats funcionando corretamente** no Radarr/Sonarr
- ✅ **Melhor experiência na automação** de downloads
- ✅ **Priorização inteligente** de releases em português brasileiro

## Padronizações Aplicadas

| Original | Padronizado |
|----------|-------------|
| `DUAL`, `Dual Ãudio` | `BRAZILIAN-DUAL-AUDIO` |
| `Dublado` | `DUBLADO` |
| `Nacional` | `NACIONAL` |
| `Legendado` | `LEGENDADO` |

## 💚 Reconhecimento

Nosso profundo agradecimento a todas as comunidades de trackers brasileiros pelo trabalho contínuo e dedicado. Esta customização apenas adiciona uma camada de padronização técnica para facilitar a automação, preservando totalmente a qualidade e integridade dos releases originais.

---

## 🚀 Resultado

Com estes indexers customizados, você terá acesso ao excelente conteúdo disponibilizado pelas comunidades brasileiras com a vantagem adicional de uma nomenclatura padronizada, garantindo uma experiência superior na automação de mídia em português brasileiro.

## Instalação

### 1. Localize a pasta de definições do Prowlarr
```bash
# Docker
/config/Definitions/Custom # Se não houver a pasta Custom, crie manualmente.

# Windows
C:\ProgramData\Prowlarr\Definitions\Custom # Se não houver a pasta Custom, crie manualmente.

# Linux
~/.config/Prowlarr/Definitions/Custom # Se não houver a pasta Custom, crie manualmente.
```

### 2. Adicione os arquivos `.yml` nesta pasta

Copie os indexers customizados para o diretório `/config/Definitions/Custom`

### 3. Reinicie o Prowlarr
```bash
docker restart prowlarr
```

### 4. Configure os indexers no Prowlarr

Acesse **Indexers** → **Add Indexer** e procure pelos indexers com nomes "trashguides-pt-br. e desativa os padores do Prowlarr para estes indexes.

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
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/iac/docker-compose/manual/docker-compose.yaml -o docker-compose.yaml
```
Obs: Ja efetua o download do docker compose. e também ja tem criado o script para baixar os custom formats, caso queira baixa-lo, use este script abaixo:

```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/iac/docker-compose/manual/docker-compose.yaml -o docker-compose.yaml

#Script de Download dos Custom Formats
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/iac/docker-compose/manual/download-custom-formats.sh -o download-custom-formats.sh

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
> **Dica:** Baixe apenas UM config.yaml, de acordo com o perfil. ( Também há perfis sem Animes. 

```bash
# Opção 1: Legendados Sem HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO.yaml \
  -o config/config.yml

# Opção 2: Legendados COM HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-HDR-ON.yaml \
  -o config/config.yml

# Opção 3: Dublados sem HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO.yaml \
  -o config/config.yml

# Opção 4: Dublados Com HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-HDR-ON.yaml \
  -o config/config.yml

# Opção 5: Legendados Sem HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-SEM-ANIMES.yaml \
  -o config/config.yml 

# Opção 6: Legendados COM HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-HDR-ON-SEM-ANIMES.yaml \
  -o config/config.yml

# Opção 7: Dublados sem HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-SEM-ANIMES.yaml \
  -o config/config.yml

# Opção 8: Dublados Com HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-HDR-ON-SEM-ANIMES.yaml \
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

BASE_URL="https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/custom-formats"

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
download_format 'custom-pt-br-dual-audio.json'
download_format 'custom-pt-br-dual-language.json'
download_format 'custom-pt-br-dublado-language.json'
download_format 'custom-pt-br-dublado.json'
download_format 'custom-pt-br-legendado.json'
download_format 'custom-pt-br-original-language.json'
download_format 'custom-pt-br-web-tier-bad-group.json'
download_format 'custom-pt-br-web-tier.json'


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
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/iac/docker-compose/automatico/docker-compose.yaml -o docker-compose.yaml
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
# Opção 1: Legendados Sem HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO.yaml \
  -o config/config.yml

# Opção 2: Legendados COM HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-HDR-ON.yaml \
  -o config/config.yml

# Opção 3: Dublados sem HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO.yaml \
  -o config/config.yml

# Opção 4: Dublados Com HDR
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-HDR-ON.yaml \
  -o config/config.yml

# Opção 5: Legendados Sem HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-SEM-ANIMES.yaml \
  -o config/config.yml 

# Opção 6: Legendados COM HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-LEGENDADO-HDR-ON-SEM-ANIMES.yaml \
  -o config/config.yml

# Opção 7: Dublados sem HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-SEM-ANIMES.yaml \
  -o config/config.yml

# Opção 8: Dublados Com HDR - SEM ANIMES
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/configarr/config-DUBLADO-HDR-ON-SEM-ANIMES.yaml \
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
      BASE_URL='https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/custom-formats'
      
      # Criar diretório se não existir
      mkdir -p /config/custom-formats
      
      echo '📥 Baixando custom formats...'
      
      # Função para baixar com tratamento de erro
      download_format() {
          local file=$$1
          echo '  → '$$file
          curl -fsSL "$$BASE_URL/$$file" -o "/config/custom-formats/$$file" || {
              echo '❌ Erro ao baixar '$$file
              return 1
          }
      }
      
		# Custom Formats Globais
		download_format 'custom-pt-br-dual-audio.json'
		download_format 'custom-pt-br-dual-language.json'
		download_format 'custom-pt-br-dublado-language.json'
		download_format 'custom-pt-br-dublado.json'
		download_format 'custom-pt-br-legendado.json'
		download_format 'custom-pt-br-original-language.json'
		download_format 'custom-pt-br-web-tier-bad-group.json'
		download_format 'custom-pt-br-web-tier.json'
      
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
                  
                  BASE_URL="https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/refs/heads/develop/custom-formats"
                  
                  # Função para download com retry
                  download_format() {
                    local file=$1
                    echo "  → Baixando: $file"
                    curl -fsSL --retry 3 --retry-delay 2 "$BASE_URL/$file" \
                      -o "/config/custom_formats/$file" || {
                      echo "❌ Erro ao baixar $file"
                      return 1
                    }
                  }
                  
						# Custom Formats Globais
						download_format 'custom-pt-br-dual-audio.json'
						download_format 'custom-pt-br-dual-language.json'
						download_format 'custom-pt-br-dublado-language.json'
						download_format 'custom-pt-br-dublado.json'
						download_format 'custom-pt-br-legendado.json'
						download_format 'custom-pt-br-original-language.json'
						download_format 'custom-pt-br-web-tier-bad-group.json'
						download_format 'custom-pt-br-web-tier.json'
                  
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