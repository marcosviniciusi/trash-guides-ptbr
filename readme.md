# TRaSH Guides PT-BR - Custom Formats

Custom Formats em Português Brasileiro para Radarr e Sonarr, otimizados para conteúdo nacional e dublagens/legendas PT-BR.

[![Configarr Compatible](https://img.shields.io/badge/Configarr-Compatible-green)](https://github.com/raydak-labs/configarr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Índice

- [Sobre](## 🎯 Sobre)
- [Custom Formats Disponíveis](## 📦 Custom Formats Disponíveis)
- [Instalação Manual](## 🔧 Instalação Manual)
- [🤖 O que é o Configarr?](## 🤖 O que é o Configarr?)
  - [Docker Compose](## 🐳 Docker Compose)
  - [Kubernetes](##kubernetes)
- [Estrutura de Scores](##estrutura-de-scores)
- [Contribuindo](##contribuindo)

## 🎯 Sobre

Este repositório contém Custom Formats personalizados para priorizar:
- ✅ Conteúdo dublado/legendado em PT-BR
- ✅ Releases de grupos brasileiros confiáveis
- ✅ Qualidade adequada para conteúdo nacional
- ✅ Filtros específicos para animes com foco em PT-BR
- ✅ Compatível com Configarr para sincronização automática

Estes formatos são complementares aos [TRaSH Guides oficiais](https://trash-guides.info/), não substitutos.

## 📦 Custom Formats Disponíveis

### 🎬 Radarr (Filmes)

#### Web Tier PT-BR
| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) de grupos confiáveis | +6000 (Filmes) |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado ou dublado) | +5500 (Filmes) |
| **custom-web-tier-ptbr-not-group-radarr** |  Prioriza Releases PT-BR Não Mapeados| +5000 (Filmes) |

#### Animes (Radarr)
| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) de grupos confiáveis | +60000000 (Animes) |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR (legendado ou dublado) | +55000000 (Animes) |
| **custom-web-tier-ptbr-not-group-radarr** |  Prioriza Releases PT-BR Não Mapeados | +50000000 (Animes) |
| **custom-animes-toonshub-ptbr-radarr** | Prioriza releases ToonsHub PT-BR | +750000 |
| **custom-animes-toonshub-pt-radarr** | Prioriza releases ToonsHub PT | +700000 |
| **custom-animes-not-brazilian-radarr** | Penaliza releases sem PT-BR | -100000 |
| **custom-animes-not-original-radarr** | Penaliza áudio não original (duplas legendas, etc) | -100000 |
| **custom-animes-not-portuguese-radarr** | Penaliza conteúdo sem português | -100000 |


### 📺 Sonarr (Séries)

#### Web Tier PT-BR
| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) | +7000 (Séries) |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR | +6500 (Séries) |
| **custom-web-tier-ptbr-not-group-sonarr** | Prioriza Releases PT-BR Não Mapeados | +6000 (Séries) |

#### Animes (Sonarr)
| Custom Format | Descrição | Score Recomendado |
|---------------|-----------|-------------------|
| **custom-web-tier-ptbr-dual** | Prioriza áudio dual (PT-BR + Original) | +60000000 (Animes) |
| **custom-web-tier-ptbr-not-dual** | Prioriza apenas PT-BR | +6500 (Séries) / +55000000 (Animes) |
| **custom-web-tier-ptbr-not-group-sonarr** | Prioriza Releases PT-BR Não Mapeados | +50000000 (Animes) |
| **custom-animes-toonshub-ptbr-sonarr** | Prioriza ToonsHub PT-BR | +750000 |
| **custom-animes-toonshub-pt-sonarr** | Prioriza ToonsHub PT | +700000 |
| **custom-animes-not-brazilian-sonarr** | Penaliza releases sem PT-BR | -10000 |
| **custom-animes-not-original-sonarr** | Penaliza áudio não original | -10000 |
| **custom-animes-not-portuguese-sonarr** | Penaliza sem português | -10000 |


## 🔧 Instalação Manual

### Via Interface Web
### Pré-requisito: Criar Quality Profile "HD"

Antes de configurar os custom formats, você precisa ter um Quality Profile chamado **"HD"** (ou ajustar o nome no `config.yml`).

### Criado O Profile com Nome "HD" ###

#### No Radarr/Sonarr:

1. Acesse **Settings → Profiles**
2. Clique em **+** para adicionar novo perfil
3. Configure:
   - **Name**: `HD`
   - **Upgrades Allowed**: ✅ (habilitado)
   - **Upgrade Until**: Selecione a qualidade máxima desejada (ex: Bluray-1080p)
   - **Qualities**: Selecione as qualidades que deseja (recomendado: WEBDL-1080p, WEBRip-1080p, Bluray-1080p, Remux-1080p)
   - **Minimum Custom Format Score**: `0` (ou deixe em branco)
4. Clique em **Save**

### Adicionando manualmente os Custom Formats
#### No Radarr/Sonarr:
1. Acesse **Settings → Custom Formats**
2. Clique em **+** para adicionar novo formato
3. Cole o conteúdo do JSON desejado
4. Salve e configure o score no Quality Profile

## 🤖 O que é o Configarr?

[Configarr](https://github.com/raydak-labs/configarr) é uma ferramenta de automação e sincronização para Radarr e Sonarr que permite gerenciar **Custom Formats**, **Quality Definitions** e **Quality Profiles** através de arquivos de configuração (YAML).

### Como funciona?

Em vez de configurar manualmente cada Custom Format pela interface web (copiando e colando JSONs um por um), o Configarr:

1. 📥 **Lê** um arquivo de configuração centralizado (`config.yml`)
2. 🔍 **Busca** os Custom Formats especificados (localmente ou de repositórios)
3. 🔄 **Sincroniza** automaticamente com suas instâncias do Radarr/Sonarr
4. 🎯 **Aplica** os scores definidos nos Quality Profiles
5. ✅ **Atualiza** tudo de forma idempotente (pode rodar quantas vezes quiser)

### 🎯 Principais Vantagens

#### 1. **Configuração como Código (IaC)**
```yaml
# Tudo em um arquivo config.yml versionável
radarr:
  movies:
    custom_formats:
      - trash_ids:
          - custom-web-tier-ptbr-dual
        assign_scores_to:
          - name: HD
            score: 6000
```
- ✅ Versionamento com Git
- ✅ Fácil de fazer backup
- ✅ Documentação integrada
- ✅ Reproduzível em qualquer ambiente

#### 2. **Sincronização Automática**

Sem Configarr:
```
1. Baixar JSON
2. Abrir Radarr → Settings → Custom Formats
3. Clicar em "+"
4. Copiar e colar o JSON
5. Salvar
6. Abrir Settings → Profiles
7. Rolar até o Custom Format
8. Digitar o score manualmente
9. Salvar
10. Repetir para cada Custom Format (15x? 20x? 😫)
```

Com Configarr:
```bash
docker run ghcr.io/raydak-labs/configarr:latest
# Pronto! ✨
```

## Como Configura-lo?

### Pré-requisitos

- [Configarr](https://github.com/raydak-labs/configarr) instalado
- API Keys do Radarr/Sonarr
- Docker ou Kubernetes

---

## 🐳 Docker Compose

### 1. Estrutura de Diretórios
```bash
mkdir -p configarr/{config,secrets,custom_formats}
cd configarr
```

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

### 3. Criar config.yml
```bash
# Baixe o exemplo completo do repositório
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/config.yml \
  -o config/config.yml
```

Ou crie manualmente:
```yaml
localCustomFormatsPath: /config/custom_formats
telemetry: true

radarr:
  movies:
    base_url: !secret RADARR_URL
    api_key: !secret RADARR_API_KEY
    
    custom_formats:
      - trash_ids:
          - custom-web-tier-ptbr-dual
          - custom-web-tier-ptbr-not-dual
          - custom-web-tier-ptbr-not-group-radarr
        assign_scores_to:
          - name: HD
            score: 6000

# [Veja config.yml completo no repositório]
```

### 4. Script de Download dos Custom Formats
```bash
cat > download-custom-formats.sh << 'EOF'
#!/bin/bash

echo "Downloading custom formats..."
mkdir -p custom_formats

# Radarr Formats
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-dual.json \
  -o custom_formats/custom-web-tier-ptbr-dual.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-dual.json \
  -o custom_formats/custom-web-tier-ptbr-not-dual.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-group-radarr.json \
  -o custom_formats/custom-web-tier-ptbr-not-group-radarr.json

# Sonarr Formats
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-group-sonarr.json \
  -o custom_formats/custom-web-tier-ptbr-not-group-sonarr.json

# Animes Sonarr
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-brazilian-sonarr.json \
  -o custom_formats/custom-animes-not-brazilian-sonarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-original-sonarr.json \
  -o custom_formats/custom-animes-not-original-sonarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-portuguese-sonarr.json \
  -o custom_formats/custom-animes-not-portuguese-sonarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-pt-sonarr.json \
  -o custom_formats/custom-animes-toonshub-pt-sonarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-ptbr-sonarr.json \
  -o custom_formats/custom-animes-toonshub-ptbr-sonarr.json

# Animes Radarr
curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-brazilian-radarr.json \
  -o custom_formats/custom-animes-not-brazilian-radarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-original-radarr.json \
  -o custom_formats/custom-animes-not-original-radarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-portuguese-radarr.json \
  -o custom_formats/custom-animes-not-portuguese-radarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-pt-radarr.json \
  -o custom_formats/custom-animes-toonshub-pt-radarr.json

curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-ptbr-radarr.json \
  -o custom_formats/custom-animes-toonshub-ptbr-radarr.json

echo "Custom formats downloaded successfully!"
EOF

chmod +x download-custom-formats.sh
./download-custom-formats.sh
```

### 5. Docker Compose - Execução Manual
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

### 6. Docker Compose - Execução Agendada e sincronização dos Releases do Repo (com Ofelia)
```yaml
version: '3.8'

services:
  # Download dos Custom Formats
  download-formats:
    image: curlimages/curl:latest
    container_name: configarr-download
    command: >
      sh -c "
      mkdir -p /config/custom_formats &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-dual.json -o /config/custom_formats/custom-web-tier-ptbr-dual.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-dual.json -o /config/custom_formats/custom-web-tier-ptbr-not-dual.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-group-radarr.json -o /config/custom_formats/custom-web-tier-ptbr-not-group-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-group-sonarr.json -o /config/custom_formats/custom-web-tier-ptbr-not-group-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-brazilian-sonarr.json -o /config/custom_formats/custom-animes-not-brazilian-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-original-sonarr.json -o /config/custom_formats/custom-animes-not-original-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-portuguese-sonarr.json -o /config/custom_formats/custom-animes-not-portuguese-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-pt-sonarr.json -o /config/custom_formats/custom-animes-toonshub-pt-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-ptbr-sonarr.json -o /config/custom_formats/custom-animes-toonshub-ptbr-sonarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-brazilian-radarr.json -o /config/custom_formats/custom-animes-not-brazilian-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-original-radarr.json -o /config/custom_formats/custom-animes-not-original-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-not-portuguese-radarr.json -o /config/custom_formats/custom-animes-not-portuguese-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-pt-radarr.json -o /config/custom_formats/custom-animes-toonshub-pt-radarr.json &&
      curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-animes-toonshub-ptbr-radarr.json -o /config/custom_formats/custom-animes-toonshub-ptbr-radarr.json &&
      echo 'Custom formats downloaded successfully!'
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
  
  # Scheduler
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

### 7. Executar
```bash
# Execução manual (uma vez)
docker-compose up configarr

# Com scheduler (agendado)
docker-compose up -d

# Ver logs
docker-compose logs -f configarr

# Forçar execução manual do job
docker exec configarr /app/configarr

# Atualizar custom formats
./download-custom-formats.sh
docker-compose restart configarr
```

---

## ☸️ Kubernetes

### 1. Estrutura de Secrets

Crie um arquivo `secrets.yml`:
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

### 2. Aplicar Recursos
```bash
# Criar ConfigMap
kubectl create configmap configarr-config \
  --from-file=config.yml \
  -n NAMESPACE

# Criar Secret
kubectl create secret generic configarr \
  --from-literal=secrets_yml="$(cat secrets.yml)" \
  -n NAMESPACE

# Ou via Infisical (recomendado)
kubectl apply -f infisical-secret.yaml
```

### 3. CronJob Kubernetes
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: configarr-sync
  namespace: NAMESPACE
spec:
  schedule: "0 2 * * *"  # Todo dia às 2h da manhã
  successfulJobsHistoryLimit: 1
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          initContainers:
            - name: download-custom-formats
              image: curlimages/curl:latest
              command:
                - sh
                - -c
                - |
                  echo "Downloading custom formats..."
                  mkdir -p /config/custom_formats
                  
                  curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-dual.json \
                    -o /config/custom_formats/custom-web-tier-ptbr-dual.json
                  
                  curl -fsSL https://raw.githubusercontent.com/marcosviniciusi/trash-guides-ptbr/main/custom-formats/custom-web-tier-ptbr-not-dual.json \
                    -o /config/custom_formats/custom-web-tier-ptbr-not-dual.json
                  
                  # [Adicione todos os outros curls aqui]
                  
                  echo "Custom formats downloaded successfully!"
              
              volumeMounts:
                - name: custom-formats-storage
                  mountPath: /config
          
          containers:
            - name: configarr
              image: ghcr.io/raydak-labs/configarr:latest
              imagePullPolicy: Always
              env:
                - name: LOG_STACKTRACE
                  value: "true"
                - name: OTEL_LOG_LEVEL
                  value: "debug"
              volumeMounts:
                - name: configarr-config
                  mountPath: /app/config/config.yml
                  subPath: config.yml
                - name: secrets
                  mountPath: /app/config/secrets.yml
                  subPath: secrets_yml
                - name: custom-formats-storage
                  mountPath: /config
                  readOnly: true

          restartPolicy: Never
          volumes:
            - name: custom-formats-storage
              emptyDir: {}
            - name: configarr-config
              configMap:
                name: configarr-config
            - name: secrets
              secret:
                secretName: configarr
```

### 4. Aplicar e Testar
```bash
# Aplicar o CronJob
kubectl apply -f configarr-cronjob.yaml

# Testar manualmente
kubectl create job --from=cronjob/configarr-sync configarr-test -n NAMESPACE

# Ver logs
kubectl logs -f job/configarr-test -n NAMESPACE

# Ver status
kubectl get cronjob configarr-sync -n NAMESPACE
```

---

## 📊 Estrutura de Scores

### Filmes/Series (Radarr/Sonarr)
- **Áudio de Alta Qualidade**: 1000-5000
- **Custom Formats PT-BR**: 5000-6000
- **Remux/Bluray Tiers**: 1700-1950
- **Penalizações**: -10000 a -100000

### Animes (Radarr/Sonarr)
- **ToonsHub PT-BR**: +750000
- **ToonsHub PT**: +700000
- **Web Tier PT-BR Dual**: +60000000
- **Web Tier PT-BR Not Dual**: +55000000
- **Web Tier PT-BR not-group**: +50000000
- **Sem PT-BR**: -100000

## 🔄 Atualizações Automáticas

### Docker Compose (Ofelia)
```yaml
# Diariamente às 2h
ofelia.job-exec.configarr-sync.schedule: "0 2 * * *"

# A cada 6 horas
ofelia.job-exec.configarr-sync.schedule: "0 */6 * * *"

# Toda semana no domingo às 14h
ofelia.job-exec.configarr-sync.schedule: "0 14 * * 0"
```

### Kubernetes (CronJob)
```yaml
schedule: "0 2 * * *"      # Diariamente às 2h
schedule: "0 */6 * * *"    # A cada 6 horas
schedule: "0 14 * * 0"     # Toda semana no domingo às 14h
```

## 📁 Estrutura do Repositório
```
trash-guides-ptbr/
├── README.md                                      # Este arquivo
├── config.yml                                     # Exemplo de configuração Configarr
├── docker-compose.yml                             # Docker Compose exemplo
├── custom-formats/                                # Todos os custom formats
│   ├── custom-web-tier-ptbr-dual.json
│   ├── custom-web-tier-ptbr-not-dual.json
│   ├── custom-web-tier-ptbr-not-group-radarr.json
│   ├── custom-web-tier-ptbr-not-group-sonarr.json
│   ├── custom-animes-not-brazilian-radarr.json
│   ├── custom-animes-not-brazilian-sonarr.json
│   ├── custom-animes-not-original-radarr.json
│   ├── custom-animes-not-original-sonarr.json
│   ├── custom-animes-not-portuguese-radarr.json
│   ├── custom-animes-not-portuguese-sonarr.json
│   ├── custom-animes-toonshub-pt-radarr.json
│   ├── custom-animes-toonshub-pt-sonarr.json
│   ├── custom-animes-toonshub-ptbr-radarr.json
│   └── custom-animes-toonshub-ptbr-sonarr.json
└── kubernetes/
    ├── configarr-cronjob.yaml
    └── infisical-secret.yaml
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para adicionar novos custom formats ou melhorias.

1. Fork este repositório
2. Crie um branch (`git checkout -b feature/novo-formato`)
3. Adicione o custom format na pasta `custom-formats/`
4. Teste com Radarr/Sonarr
5. Atualize este README
6. Commit (`git commit -am 'Adiciona formato XYZ'`)
7. Push (`git push origin feature/novo-formato`)
8. Abra um Pull Request

### Padrão de Nomenclatura

- **custom-web-tier-ptbr-*.json** - Formatos para web releases PT-BR
- **custom-animes-*.json** - Formatos específicos para animes
- Prefixo `custom-` para diferenciar dos oficiais do TRaSH
- Sufixo `-radarr` ou `-sonarr` para especificar a aplicação

## ❓ FAQ

**P: Esses formatos substituem os TRaSH Guides?**  
R: Não, eles complementam. Use ambos para melhores resultados.

**P: Preciso usar todos os custom formats?**  
R: Não, escolha os que fazem sentido para seu caso de uso.

**P: Como atualizo os custom formats?**  
R: O Configarr sincroniza automaticamente quando executado. Configure um CronJob/Ofelia para atualizações periódicas.

**P: Posso usar sem Docker/Kubernetes?**  
R: Sim! Instale o Configarr localmente e execute manualmente.

**P: Os scores são obrigatórios?**  
R: Não, ajuste conforme suas preferências. Os scores sugeridos são apenas recomendações.

**P: Como funciona o Ofelia?**  
R: Ofelia é um scheduler de jobs para Docker. Ele executa comandos em containers baseado em agendamentos cron.

## 📝 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Créditos

- Baseado no trabalho incrível do [TRaSH Guides](https://trash-guides.info/)
- Desenvolvido para a comunidade brasileira de *arr apps
- Mantido por [Marcos Gabriel](https://github.com/marcosviniciusi)

---

**Dúvidas ou sugestões?** Abra uma [issue](https://github.com/marcosviniciusi/trash-guides-ptbr/issues) ou contribua com um [pull request](https://github.com/marcosviniciusi/trash-guides-ptbr/pulls)!

**⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!**