## 🔄 Autobrr Proxy PT-BR

Proxy intermediário inteligente para padronizar títulos de releases brasileiros antes de chegarem ao Radarr/Sonarr através do Autobrr.

### 📋 O que faz?

O Autobrr Proxy atua como uma **camada de tradução** entre o Autobrr e seus aplicativos *arr, interceptando releases enviados pelo Autobrr e aplicando transformações automáticas nos títulos para garantir compatibilidade perfeita com os Custom Formats PT-BR.

**Transformações aplicadas:**

| Padrão Original | Convertido Para |
|----------------|-----------------|
| `DUAL`, `Dual Áudio` | `BRAZILIAN-DUAL-AUDIO` |
| `Dublado`, `DUBLADO` | `DUBLADO` |
| `Nacional`, `NACIONAL` | `NACIONAL` |
| `Legendado`, `LEGENDADO` | `LEGENDADO` |
| `PT-BR`, `Portuguese` | `BRAZILIAN` |

### 🎯 Por que usar?

- ✅ **Padronização automática**: Unifica nomenclaturas entre diferentes trackers brasileiros
- ✅ **Custom Formats funcionam corretamente**: Garante que os CFs detectem releases PT-BR
- ✅ **Configuração dinâmica**: Suporta quantos *arr apps você precisar (1 a 99)
- ✅ **Regras por indexer**: Cada tracker brasileiro tem regras específicas otimizadas
- ✅ **Logs detalhados**: DEBUG mode mostra exatamente o que está sendo modificado
- ✅ **Zero downtime**: Proxy transparente - se falhar, Autobrr continua funcionando
- ✅ **Multi-instância**: Gerencie Movies, Series e Animes separadamente

### 🏗️ Arquitetura
```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Autobrr   │────▶│  Proxy PT-BR     │────▶│  Radarr     │
│             │     │                  │     │  Sonarr     │
│ (detecta    │     │ • Transforma     │     │  (recebe    │
│  releases)  │     │   títulos        │     │   títulos   │
│             │     │ • Aplica regras  │     │   padrões)  │
└─────────────┘     │ • Loga tudo      │     └─────────────┘
                    └──────────────────┘
```

### 📦 Docker Compose

#### Exemplo Completo (4 instâncias)
```yaml
version: '3.8'

services:
  autobrr-proxy:
    image: marcosviniciusi/autobrr-proxy-br:latest
    container_name: autobrr-proxy
    restart: unless-stopped
    ports:
      - "8888:8888"
    environment:
      # ============================================
      # CONFIGURAÇÃO GLOBAL
      # ============================================
      # LOG_LEVEL: INFO (padrão) ou DEBUG (verbose)
      - LOG_LEVEL=INFO
      
      # ============================================
      # APP 01: Radarr Movies (Filmes)
      # ============================================
      - APP_01_TYPE=radarr                    # Tipo: radarr, sonarr, lidarr, readarr, whisparr
      - APP_01_NAME=movies                    # Nome amigável (aparece nos logs)
      - APP_01_SUBPATH=radarr-movies          # Caminho do endpoint: /radarr-movies
      - APP_01_URL=https://movies.example.com # URL completa do Radarr (com porta se necessário)
      - APP_01_API_KEY=sua-api-key-radarr     # API Key do Radarr
      
      # ============================================
      # APP 02: Radarr Animes (Filmes de Anime)
      # ============================================
      - APP_02_TYPE=radarr
      - APP_02_NAME=animes-movies
      - APP_02_SUBPATH=radarr-animes
      - APP_02_URL=https://animes-movies.example.com:PORTA
      - APP_02_API_KEY=sua-api-key-radarr-animes
      
      # ============================================
      # APP 03: Sonarr Series (Séries)
      # ============================================
      - APP_03_TYPE=sonarr
      - APP_03_NAME=series
      - APP_03_SUBPATH=sonarr-series
      - APP_03_URL=https://series.example.com:PORTA
      - APP_03_API_KEY=sua-api-key-sonarr
      
      # ============================================
      # APP 04: Sonarr Animes (Séries de Anime)
      # ============================================
      - APP_04_TYPE=sonarr
      - APP_04_NAME=animes-tv
      - APP_04_SUBPATH=sonarr-animes
      - APP_04_URL=https://animes-tv.example.com:PORTA
      - APP_04_API_KEY=sua-api-key-sonarr-animes
      
      # ============================================
      # ADICIONE MAIS APPS CONFORME NECESSÁRIO
      # Formato: APP_XX_* onde XX vai de 01 a 99
      # ============================================
      # - APP_05_TYPE=whisparr
      # - APP_05_NAME=adult
      # - APP_05_SUBPATH=whisparr-adult
      # - APP_05_URL=https://whisparr.example.com
      # - APP_05_API_KEY=sua-api-key-whisparr
    
    networks:
      - media
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8888/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

networks:
  media:
    external: true
```

#### Exemplo Mínimo (1 instância)
```yaml
version: '3.8'

services:
  autobrr-proxy:
    image: marcosviniciusi/autobrr-proxy-br:latest
    container_name: autobrr-proxy
    restart: unless-stopped
    ports:
      - "8888:8888"
    environment:
      - LOG_LEVEL=INFO
      - APP_01_TYPE=radarr
      - APP_01_NAME=movies
      - APP_01_SUBPATH=radarr-movies
      - APP_01_URL=http://RADARR_IP:7878
      - APP_01_API_KEY=sua-api-key-aqui
    networks:
      - media

networks:
  media:
    external: true
```

### ⚙️ Variáveis de Ambiente

#### Configuração Global

| Variável | Descrição | Valores | Padrão |
|----------|-----------|---------|--------|
| `LOG_LEVEL` | Nível de verbosidade dos logs | `INFO`, `DEBUG` | `INFO` |

#### Configuração por App (APP_XX_*)

Cada aplicação requer 5 variáveis obrigatórias, onde `XX` é um número de `01` a `99`:

| Variável | Obrigatório | Descrição | Exemplo |
|----------|-------------|-----------|---------|
| `APP_XX_TYPE` | ✅ | Tipo de aplicação | `radarr`, `sonarr`, `lidarr`, `readarr`, `whisparr` |
| `APP_XX_NAME` | ⚠️ | Nome amigável (aparece nos logs) | `movies`, `series`, `animes-tv` |
| `APP_XX_SUBPATH` | ✅ | Caminho do endpoint no proxy | `radarr-movies`, `sonarr-series` |
| `APP_XX_URL` | ✅ | URL completa da aplicação | `https://radarr.example.com:PORTA` |
| `APP_XX_API_KEY` | ✅ | API Key da aplicação | `abc123def456...` |

**Notas importantes:**
- ⚠️ `APP_XX_NAME` é opcional, mas recomendado para logs mais claros
- 🔢 Numeração **não precisa ser sequencial** (pode usar 01, 03, 10, 15, etc)
- 📍 `APP_XX_SUBPATH` define o endpoint: `/radarr-movies`, `/sonarr-series`, etc
- 🌐 `APP_XX_URL` pode ser HTTP ou HTTPS, com ou sem porta

### ⚙️ Configuração no Autobrr

#### 1. Adicionar Download Client

**Settings → Clients → Add Download Client**

Configure **um client para cada *arr app** que você adicionou no proxy:
```
┌─────────────────────────────────────────────┐
│ Type:     Radarr (ou Sonarr)                │
│ Name:     Radarr Movies (Proxy BR)          │
│ Host:     http://autobrr-proxy:8888         │
│ Base URL: /radarr-movies                    │  ← IMPORTANTE!
│ API Key:  [mesma API key do Radarr]         │
│ Port:     (deixe vazio)                      │
└─────────────────────────────────────────────┘
```

**OU (dependendo da versão do Autobrr):**
```
┌─────────────────────────────────────────────┐
│ Type:     Radarr (ou Sonarr)                │
│ Name:     Radarr Movies (Proxy BR)          │
│ Host:     http://autobrr-proxy:8888/radarr-movies  │
│ API Key:  [mesma API key do Radarr]         │
└─────────────────────────────────────────────┘
```

#### 2. Endpoints Disponíveis

Os endpoints são criados dinamicamente baseados no `APP_XX_SUBPATH`:

| Configuração ENV | Endpoint Gerado | Use no Autobrr |
|------------------|-----------------|----------------|
| `APP_01_SUBPATH=radarr-movies` | `/radarr-movies` | `http://autobrr-proxy:8888/radarr-movies` |
| `APP_02_SUBPATH=radarr-animes` | `/radarr-animes` | `http://autobrr-proxy:8888/radarr-animes` |
| `APP_03_SUBPATH=sonarr-series` | `/sonarr-series` | `http://autobrr-proxy:8888/sonarr-series` |
| `APP_04_SUBPATH=sonarr-animes` | `/sonarr-animes` | `http://autobrr-proxy:8888/sonarr-animes` |

#### 3. Teste a Conexão

No Autobrr, clique em **Test** ao lado do client configurado. Deve aparecer:
```
✅ Connection successful
```

### 🔍 Indexers Suportados e Regras

O proxy detecta automaticamente o indexer pelo campo `indexer` enviado pelo Autobrr e aplica as regras específicas:

| Indexer | Detecção | Regras Aplicadas |
|---------|----------|------------------|
| **CapybaraBR** | `CapybaraBR`, `capybara-br` | `DUAL` → `BRAZILIAN-DUAL-AUDIO` |
| **BrasilTracker** | `BrasilTracker`, `brasil-tracker` | `Dual Audio` → `BRAZILIAN-DUAL-AUDIO`<br>`Subs/Legendado` → `LEGENDADO`<br>`Nacional` → `NACIONAL`<br>`Dublado` → `DUBLADO` |
| **Bj-Share** | `Bj-Share`, `bjshare` | `Dual Áudio` → `BRAZILIAN-DUAL-AUDIO`<br>`Legendado` → `LEGENDADO`<br>`Nacional` → `NACIONAL` |
| **AmigosShare** | `AmigosShare`, `amigos-share` | Padroniza: `dual-audio`, `dublado`, `nacional`, `legendado` |
| **Locadora** | `Locadora`, `locadora.cc` | Remove sufixos: `/ Language (Code)`<br>`DUAL-` → `BRAZILIAN-DUAL-AUDIO-`<br>Adiciona `LEGENDADO` para idiomas não-PT |
| **Samaritano** | `Samaritano` | `DUAL` → `BRAZILIAN-DUAL-AUDIO` |
| **Outros** | Qualquer indexer | Regras globais:<br>`DUAL` → `BRAZILIAN-DUAL-AUDIO`<br>`PT-BR` → `BRAZILIAN`<br>`Portuguese` → `BRAZILIAN` |

**Nota:** A detecção é **case-insensitive** e ignora espaços/hífens. Ex: `Capybara-BR` = `CapybaraBR` = `capybarabr`

### 📊 Monitoramento e Debug

#### Ver Configuração Carregada
```bash
curl http://localhost:8888/ | jq
```

**Saída:**
```json
{
  "service": "autobrr-proxy-unified",
  "version": "1.0.7",
  "indexers_supported": [
    "capybarabr",
    "brasiltracker",
    "bjshare",
    "amigosshare",
    "locadora",
    "samaritano"
  ],
  "total_apps": 4,
  "endpoints": {
    "radarr-movies": {
      "url": "http://proxy:8888/radarr-movies",
      "type": "radarr",
      "name": "movies",
      "target": "https://RADARR_IP:PORTA"
    },
    "sonarr-series": {
      "url": "http://proxy:8888/sonarr-series",
      "type": "sonarr",
      "name": "series",
      "target": "https://SONARR_IP.:PORTA"
    }
  }
}
```

#### Health Check
```bash
curl http://localhost:8888/health | jq
```

**Saída:**
```json
{
  "proxy": "ok",
  "indexers_supported": [
    "capybarabr",
    "brasiltracker",
    "bjshare",
    "amigosshare",
    "locadora",
    "samaritano"
  ],
  "apps": {
    "radarr-movies": {
      "status": "ok",
      "type": "radarr",
      "name": "movies",
      "url": "http://RADARR_IP:7878"
    },
    "sonarr-series": {
      "status": "unreachable",
      "type": "sonarr",
      "name": "series",
      "url": "http://SONARR_IP:8686",
      "error": "Connection timeout"
    }
  }
}
```

#### Logs em Tempo Real
```bash
# Ver todos os logs
docker logs -f autobrr-proxy

# Filtrar por app específico
docker logs -f autobrr-proxy | grep "radarr-movies"

# Ver apenas modificações de título
docker logs -f autobrr-proxy | grep "Title modified"
```

#### Modo DEBUG

Altere `LOG_LEVEL=DEBUG` no docker-compose e reinicie:
```bash
docker-compose down
docker-compose up -d
docker logs -f autobrr-proxy
```

**LOG_LEVEL=INFO (padrão):**
```
📥 INCOMING REQUEST
   App:      movies (radarr)
   Indexer:  REMOVED
🔧 Processing title modification...
✅ Title was modified!
   Original: Movie.2024.DUAL.BluRay-Group
   Modified: Movie.2024.BRAZILIAN-DUAL-AUDIO.BluRay-Group
```

**LOG_LEVEL=DEBUG (verbose):**
```
📥 INCOMING REQUEST
   App:      movies (radarr)
   Endpoint: /radarr-movies/api/v3/release/push
   Method:   POST
   From IP:  10.52.8.242
📋 Request Headers:
   Host: autobrr-proxy:8888
   User-Agent: autobrr
   X-Api-Key: 170e6d3f...9023
📦 Request Payload:
   {
     "title": "Movie.2024.DUAL.BluRay-Group",
     "indexer": "REMOVED",
     "downloadUrl": "https://...",
     "size": 8589934592
   }
🔧 Processing title modification...
[RADARR-MOVIES] Applied CapybaraBR rules
✅ Title was modified!
   Indexer:  REMOVED
   Original: Movie.2024.DUAL.BluRay-Group
   Modified: Movie.2024.BRAZILIAN-DUAL-AUDIO.BluRay-Group
📤 OUTGOING REQUEST
   Target URL: https://RADARR_IP:7878/api/v3/release/push
   Method:     POST
📋 Outgoing Headers:
   User-Agent: autobrr
   Content-Type: application/json
   X-Api-Key: 170e6d3f...9023
📦 Payload being sent:
   {
     "title": "Movie.2024.BRAZILIAN-DUAL-AUDIO.BluRay-Group",
     ...
   }
📨 RESPONSE RECEIVED
   Status Code: 200
   Status:      OK
✅ SUCCESS
```

### 🐛 Troubleshooting

#### ❌ Autobrr: "connection test failed: chunked line ends with bare LF"

**Causa:** Versão antiga do proxy (< 1.0.6)

**Solução:**
```bash
docker pull marcosviniciusi/autobrr-proxy-br:latest
docker-compose down && docker-compose up -d
```

#### ❌ Autobrr: "Unable to parse" no Radarr/Sonarr

**Causa:** Título do release original já está malformado (problema do tracker, não do proxy)

**Exemplos comuns:**
- Falta episódio: `Show S01 1080p` (deveria ser `S01E01`)
- Título duplicado: `Show S01E01 Show 1080p`

**Solução:** O proxy não pode consertar releases quebrados. Configure filtros no Autobrr para evitá-los.

#### ❌ Títulos não estão sendo modificados

**Diagnóstico:**

1. **Ative DEBUG:**
```bash
docker-compose down
# Edite docker-compose.yml: LOG_LEVEL=DEBUG
docker-compose up -d
docker logs -f autobrr-proxy
```

2. **Verifique o indexer detectado:**
```
🔖 Indexer: CapybaraBR  ← Nome detectado
[RADARR-MOVIES] Applied CapybaraBR rules ← Regras aplicadas
ℹ️  Title unchanged ← Não tinha DUAL no título
```

3. **Confirme que o título TEM os termos esperados:**
   - CapybaraBR: Precisa de `DUAL` no título
   - Locadora: Precisa de `/ Language (Code)` no final
   - BrasilTracker: Precisa de `Dual Audio`, `Legendado`, etc

#### ❌ API Key incorreta

**Sintoma:**
```
📨 RESPONSE RECEIVED
   Status Code: 401
   Status:      Unauthorized
```

**Solução:** Verifique a API Key no *arr app:
```
Settings → General → Security → API Key
```

Compare com a configuração no docker-compose (`APP_XX_API_KEY`)

#### ❌ Proxy não inicia

**Diagnóstico:**
```bash
docker logs autobrr-proxy
```

**Erros comuns:**

**"No apps configured":**
```
❌ No apps configured!
⛔ No apps configured. Exiting.
```
- Faltam variáveis `APP_XX_*` no docker-compose
- Verifique se pelo menos `APP_01_TYPE`, `APP_01_SUBPATH`, `APP_01_URL` e `APP_01_API_KEY` estão definidos

**"Invalid TYPE":**
```
⚠️  APP_01: Invalid TYPE 'raddarr'. Must be one of: radarr, sonarr, lidarr, readarr, whisparr. Skipping.
```
- Corrija o tipo no `APP_XX_TYPE`

**"Incomplete configuration":**
```
⚠️  APP_02: Incomplete configuration. Need TYPE, SUBPATH, URL, and API_KEY. Skipping.
```
- Falta alguma variável obrigatória

#### ❌ Autobrr não consegue acessar o proxy

**Sintoma:**
```
connection test failed: dial tcp: lookup autobrr-proxy: no such host
```

**Solução:** Certifique-se que ambos estão na mesma rede Docker:
```yaml
# docker-compose.yml do Autobrr
services:
  autobrr:
    networks:
      - media  # ← Mesma rede!

# docker-compose.yml do Proxy
services:
  autobrr-proxy:
    networks:
      - media  # ← Mesma rede!

networks:
  media:
    external: true
```

### 📈 Exemplos de Uso Real

#### Exemplo 1: Release com DUAL do Trackers pt-BR

**Input (Autobrr → Proxy):**
```json
{
  "title": "movie.2024.1080p.DUAL.BluRay.x264-ComandoFor",
  "indexer": "tracker-pt-br",
  "downloadUrl": "https://TRAKER.COM/download/55839"
}
```

**Output (Proxy → Radarr):**
```json
{
  "title": "MOVIE.2024.1080p.BRAZILIAN-DUAL-AUDIO.BluRay.x264-ComandoFor",
  "indexer": "tracker-pt-br",
  "downloadUrl": "https://TRAKER.COM/download/55839"
}
```

**Log:**
```
[RADARR-MOVIES] Applied CapybaraBR rules
✅ Title was modified!
  Indexer:  tracker-pt-br
  Original: movie.2024.1080p.DUAL.BluRay.x264-ComandoFor
  Modified: movie.2024.1080p.BRAZILIAN-DUAL-AUDIO.BluRay.x264-ComandoFor
```

#### Exemplo 2: Release legendado do Locadora

**Input:**
```json
{
  "title": "Anime.S01E13.1080p.WEB-DL.H.264.JPN-Group / Japanese (JP)",
  "indexer": "Locadora"
}
```

**Output:**
```json
{
  "title": "Anime.S01E13.1080p.WEB-DL.H.264.LEGENDADO-Group",
  "indexer": "Locadora"
}
```

**Log:**
```
[SONARR-ANIMES] Applied Locadora rules
✅ Title was modified!
  Indexer:  Locadora
  Original: Anime.S01E13.1080p.WEB-DL.H.264.JPN-Group / Japanese (JP)
  Modified: Anime.S01E13.1080p.WEB-DL.H.264.LEGENDADO-Group
```

#### Exemplo 3: Indexer desconhecido (regras globais)

**Input:**
```json
{
  "title": "Movie.2024.DUAL.WEB-DL-GenericGroup",
  "indexer": "TrackerXYZ"
}
```

**Output:**
```json
{
  "title": "Movie.2024.BRAZILIAN-DUAL-AUDIO.WEB-DL-GenericGroup",
  "indexer": "TrackerXYZ"
}
```

**Log:**
```
[RADARR-MOVIES] No specific rules for TrackerXYZ, applied global rules
✅ Title was modified!
  Indexer:  TrackerXYZ
  Original: Movie.2024.DUAL.WEB-DL-GenericGroup
  Modified: Movie.2024.BRAZILIAN-DUAL-AUDIO.WEB-DL-GenericGroup
```

### 🔐 Segurança

**API Keys nos logs:**
- Por padrão, API keys são **mascaradas** nos logs
- Aparecem como: `X-Api-Key: 170e6d3f...9023`
- Nunca são expostas por completo

**Headers sensíveis:**
- `X-Api-Key`, `Authorization`, `Token`, `Password`, `Secret` são automaticamente mascarados
- Formato: `primeiros8chars...ultimos4chars`

### 🚀 Atualizações
```bash
# Atualizar para a versão mais recente
docker pull marcosviniciusi/autobrr-proxy-br:latest
docker-compose down
docker-compose up -d

# Ver versão atual
curl http://localhost:8888/ | jq -r '.version'
```

### 🔗 Links Úteis

- **Repositório:** https://github.com/marcosviniciusi/trash-guides-ptbr
- **Docker Hub:** https://hub.docker.com/r/marcosviniciusi/autobrr-proxy-br
- **Issues:** https://github.com/marcosviniciusi/trash-guides-ptbr/issues
- **TRaSH Guides Oficiais:** https://trash-guides.info/
- **Autobrr:** https://autobrr.com/

### 💡 Dicas Pro

1. **Use nomes descritivos em `APP_XX_NAME`** para facilitar leitura dos logs
2. **Ative DEBUG temporariamente** quando adicionar novos indexers
3. **Monitore o health check** periodicamente para detectar problemas
4. **Crie alertas** no Uptime Kuma ou similar para o endpoint `/health`
5. **Backup do docker-compose.yml** com todas as configurações

---

**🎉 Pronto! Seu Autobrr agora envia títulos padronizados para os *arr apps!**