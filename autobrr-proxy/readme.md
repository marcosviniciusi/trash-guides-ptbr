## 🔄 Autobrr Proxy PT-BR

Proxy intermediário inteligente para padronizar títulos de releases brasileiros antes de chegarem ao Radarr/Sonarr através do Autobrr.

### 📋 O que faz?

O Autobrr Proxy atua como uma **camada de tradução** entre o Autobrr e seus aplicativos *arr, interceptando releases enviados pelo Autobrr e aplicando transformações automáticas nos títulos para garantir compatibilidade perfeita com os Custom Formats PT-BR.

**Transformações aplicadas:**

| Padrão Original | Convertido Para |
|----------------|-----------------|
| `DUAL`, `MULTI`, `Dual Áudio` | `BRAZILIAN-DUAL-AUDIO` |
| `Dublado`, `DUBLADO` | `DUBLADO` |
| `Nacional`, `NACIONAL` | `NACIONAL` |
| `Legendado`, `LEGENDADO` | `LEGENDADO` |
| `Portuguese`, `Brazil`, `PT-BR` | Adiciona `LEGENDADO` |
| Títulos com pontos (`.`) | Converte para espaços preservando padrões técnicos |
| `[Colchetes]` (UniOtaku) | Remove colchetes e adiciona `LEGENDADO` |
| `-NoGroup` (Samaritano) | Substitui por `-SAMARITANO` |

### 🎯 Por que usar?

- ✅ **Padronização automática**: Unifica nomenclaturas entre diferentes trackers brasileiros
- ✅ **Custom Formats funcionam corretamente**: Garante que os CFs detectem releases PT-BR
- ✅ **Configuração dinâmica**: Suporta quantos *arr apps você precisar (1 a 99)
- ✅ **Regras por indexer**: Cada tracker brasileiro tem regras específicas otimizadas
- ✅ **Normalização de títulos**: Remove pontos e padroniza formatação
- ✅ **Logs detalhados**: DEBUG mode mostra exatamente o que está sendo modificado
- ✅ **Zero downtime**: Proxy transparente - se falhar, Autobrr continua funcionando
- ✅ **Multi-instância**: Gerencie Movies, Series e Animes separadamente

### 🏗️ Arquitetura
```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Autobrr   │────▶│  Proxy PT-BR     │────▶│  Radarr     │
│             │     │                  │     │  Sonarr     │
│ (detecta    │     │ • Normaliza      │     │  (recebe    │
│  releases)  │     │   pontos         │     │   títulos   │
│             │     │ • Transforma     │     │   padrões)  │
│             │     │   títulos        │     │             │
│             │     │ • Aplica regras  │     │             │
│             │     │ • Loga tudo      │     │             │
└─────────────┘     └──────────────────┘     └─────────────┘
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
      - APP_02_URL=https://animes-movies.example.com:443
      - APP_02_API_KEY=sua-api-key-radarr-animes
      
      # ============================================
      # APP 03: Sonarr Series (Séries)
      # ============================================
      - APP_03_TYPE=sonarr
      - APP_03_NAME=series
      - APP_03_SUBPATH=sonarr-series
      - APP_03_URL=https://series.example.com:443
      - APP_03_API_KEY=sua-api-key-sonarr
      
      # ============================================
      # APP 04: Sonarr Animes (Séries de Anime)
      # ============================================
      - APP_04_TYPE=sonarr
      - APP_04_NAME=animes-tv
      - APP_04_SUBPATH=sonarr-animes
      - APP_04_URL=https://animes-tv.example.com:443
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
      - APP_01_URL=http://radarr:7878
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
| `APP_XX_URL` | ✅ | URL completa da aplicação | `https://radarr.example.com:443` |
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

O proxy detecta automaticamente o indexer pelo campo `indexer` enviado pelo Autobrr e aplica as regras específicas.

**⚠️ IMPORTANTE: Nomes dos Indexers no Autobr**

Para que o proxy funcione corretamente, os indexers **devem ser configurados** no Autobrr com os seguintes nomes **EXATOS** (case-insensitive):

| Indexer no Autobrr | Nomes Aceitos | Regras Aplicadas |
|---------------------|---------------|------------------|
| **CapybaraBR** | `CapybaraBR`, `capybara-br`, `capybarabr` | • `DUAL` → `BRAZILIAN-DUAL-AUDIO` |
| **BrasilTracker** | `BrasilTracker`, `brasil-tracker`, `brasiltracker` | • `Dual Audio` → `BRAZILIAN-DUAL-AUDIO`<br>• `Subs/Legendado` → `LEGENDADO`<br>• `Nacional` → `NACIONAL`<br>• `Dublado` → `DUBLADO` |
| **Bj-Share** | `Bj-Share`, `bjshare`, `bj-share` | • `Dual Áudio` → `BRAZILIAN-DUAL-AUDIO`<br>• `Legendado` → `LEGENDADO`<br>• `Nacional` → `NACIONAL` |
| **AmigosShare** | `AmigosShare`, `amigos-share`, `amigosshare` | • `dual-audio` → `BRAZILIAN-DUAL-AUDIO`<br>• `dublado` → `DUBLADO`<br>• `nacional` → `NACIONAL`<br>• `legendado` → `LEGENDADO`<br>• Sem marcador BR + sem grupo → adiciona `-ASC` |
| **Locadora** | `Locadora`, `locadora.cc`, `locadora` | • Remove sufixos: `/ Language (Code)`<br>• `DUAL-` → `BRAZILIAN-DUAL-AUDIO-`<br>• Adiciona `LEGENDADO` para idiomas não-PT<br>• Remove `-JPN` |
| **Samaritano** | `Samaritano`, `samaritano` | • `DUAL` → `BRAZILIAN-DUAL-AUDIO`<br>• `MULTI` → `BRAZILIAN-DUAL-AUDIO`<br>• `-NoGroup` → `-SAMARITANO`<br>• Sem grupo → adiciona `-SAMARITANO` |
| **UniOtaku** | `UniOtaku`, `uniotaku` | • Remove TODOS os colchetes `[xxx]`<br>• Adiciona `LEGENDADO` antes do release group |
| **Outros** | Qualquer outro nome | • Detecta padrões PT-BR explícitos<br>• Adiciona `LEGENDADO` quando apropriado<br>• NÃO converte `DUAL` genérico |

**Como configurar no autobrr:**
```
Autobrr → Indexers → [Seu Indexer] → Nome do Indexer
                                       └─> Use exatamente: CapybaraBR
                                                          BrasilTracker
                                                          Bj-Share
                                                          AmigosShare
                                                          Locadora
                                                          Samaritano
                                                          UniOtaku
```

**Nota:** A detecção é **case-insensitive** e ignora espaços/hífens internos. Exemplos válidos:
- `CapybaraBR` = `capybarabr` = `Capybara-BR` ✅
- `BrasilTracker` = `brasiltracker` = `Brasil-Tracker` ✅
- `Bj-Share` = `bjshare` = `BJ-SHARE` ✅

### 🔄 Normalização de Títulos

O proxy aplica normalização automática em **todos** os títulos antes de aplicar regras específicas:

#### Conversão de Pontos para Espaços

**Substitui pontos (`.`) por espaços, EXCETO:**
- ✅ Extensões de arquivo: `.mkv`, `.mp4`, `.avi`, `.m4v`, `.ts`, `.m2ts`
- ✅ Codecs de vídeo: `H.264`, `H.265`, `x264`, `x265`, `h264`, `h265`
- ✅ Codecs de áudio: `DDP5.1`, `DD 5.1`, `AAC2.0`, `AC3 5.1`, `E-AC3 5.1`
- ✅ DTS variants: `DTS 5.1`, `DTS:X 7.1`, `DTS-HD MA 7.1`
- ✅ Outros áudios: `TrueHD 7.1`, `Atmos 7.1`, `FLAC 2.0`
- ✅ Versões: `v2`, `v3`

**Exemplos:**
```
Input:  Its.Florida.Man.S02E04.1080p.WEB-DL.DDP5.1.H.264-STC.mkv
Output: Its Florida Man S02E04 1080p WEB-DL DDP5.1 H.264-STC.mkv

Input:  Die.Simpsons.S16E16.German.DL.1080p.WebHD.H264-RWF
Output: Die Simpsons S16E16 German DL 1080p WebHD H264-RWF

Input:  Movie.2024.1080p.BluRay.DD 5.1.x265-Group
Output: Movie 2024 1080p BluRay DD 5.1 x265-Group
```

### 📊 Monitoramento e Debug

#### Ver Configuração Carregada
```bash
curl http://localhost:8888/ | jq
```

**Saída:**
```json
{
  "service": "autobrr-proxy-unified",
  "version": "1.1.0",
  "indexers_supported": [
    "capybarabr",
    "brasiltracker",
    "bjshare",
    "amigosshare",
    "locadora",
    "samaritano",
    "uniotaku"
  ],
  "total_apps": 4,
  "endpoints": {
    "radarr-movies": {
      "url": "http://proxy:8888/radarr-movies",
      "type": "radarr",
      "name": "movies",
      "target": "https://movies.example.com:443"
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
    "samaritano",
    "uniotaku"
  ],
  "apps": {
    "radarr-movies": {
      "status": "ok",
      "type": "radarr",
      "name": "movies",
      "url": "https://movies.example.com:443"
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
   Indexer:  CapybaraBR
🔧 Processing title modification...
✅ Title was modified!
   Original: Movie.2024.DUAL.BluRay-Group
   Modified: Movie 2024 BRAZILIAN-DUAL-AUDIO BluRay-Group
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
     "indexer": "CapybaraBR",
     "downloadUrl": "https://...",
     "size": 8589934592
   }
🔧 Processing title modification...
[RADARR-MOVIES] Applied CapybaraBR rules
✅ Title was modified!
   Indexer:  CapybaraBR
   Original: Movie.2024.DUAL.BluRay-Group
   Modified: Movie 2024 BRAZILIAN-DUAL-AUDIO BluRay-Group
📤 OUTGOING REQUEST
   Target URL: https://movies.example.com:443/api/v3/release/push
   Method:     POST
📨 RESPONSE RECEIVED
   Status Code: 200
   Status:      OK
✅ SUCCESS
```

#### ❌ Títulos não estão sendo modificados

**Diagnóstico:**

1. **Verifique o nome do indexer no autobrr:**
```bash
# Verifique se o nome está correto
curl http://localhost:8888/ | jq '.indexers_supported'

# Deve retornar:
[
  "capybarabr",
  "brasiltracker",
  "bjshare",
  "amigosshare",
  "locadora",
  "samaritano",
  "uniotaku"
]
```

Se o seu indexer não aparece nessa lista, **renomeie no autobrr** para um dos nomes aceitos.

2. **Ative DEBUG:**
```bash
docker-compose down
# Edite docker-compose.yml: LOG_LEVEL=DEBUG
docker-compose up -d
docker logs -f autobrr-proxy
```

3. **Verifique o indexer detectado:**
```
🔖 Indexer: CapybaraBR  ← Nome detectado
[RADARR-MOVIES] Applied CapybaraBR rules ← Regras aplicadas
ℹ️  Title unchanged ← Não tinha DUAL no título
```

4. **Confirme que o título TEM os termos esperados:**
   - CapybaraBR: Precisa de `DUAL` no título
   - Locadora: Precisa de `/ Language (Code)` no final
   - BrasilTracker: Precisa de `Dual Audio`, `Legendado`, etc
   - UniOtaku: Precisa de `[colchetes]` para remover

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

#### Exemplo 1: Release com DUAL do CapybaraBR

**Input (Autobrr → Proxy):**
```json
{
  "title": "Dune.Part.Two.2024.1080p.DUAL.BluRay.x264-ComandoFor",
  "indexer": "CapybaraBR",
  "downloadUrl": "https://capybarabr.com/download/55839"
}
```

**Output (Proxy → Radarr):**
```json
{
  "title": "Dune Part Two 2024 1080p BRAZILIAN-DUAL-AUDIO BluRay x264-ComandoFor",
  "indexer": "CapybaraBR",
  "downloadUrl": "https://capybarabr.com/download/55839"
}
```

**Log:**
```
[RADARR-MOVIES] Applied CapybaraBR rules
✅ Title was modified!
  Indexer:  CapybaraBR
  Original: Dune.Part.Two.2024.1080p.DUAL.BluRay.x264-ComandoFor
  Modified: Dune Part Two 2024 1080p BRAZILIAN-DUAL-AUDIO BluRay x264-ComandoFor
```

#### Exemplo 2: Release do UniOtaku com colchetes

**Input:**
```json
{
  "title": "Undead Unluck: Winter-hen [WEB][1080P][H264][DD+] [GAIA Fansub]",
  "indexer": "UniOtaku"
}
```

**Output:**
```json
{
  "title": "Undead Unluck: Winter-hen WEB 1080P H264 DD+ GAIA LEGENDADO Fansub",
  "indexer": "UniOtaku"
}
```

**Log:**
```
[SONARR-ANIMES] Applied UniOtaku rules
✅ Title was modified!
  Indexer:  UniOtaku
  Original: Undead Unluck: Winter-hen [WEB][1080P][H264][DD+] [GAIA Fansub]
  Modified: Undead Unluck: Winter-hen WEB 1080P H264 DD+ GAIA LEGENDADO Fansub
```

#### Exemplo 3: Release do Samaritano sem grupo

**Input:**
```json
{
  "title": "Movie 2024 MULTI 1080p BluRay",
  "indexer": "Samaritano"
}
```

**Output:**
```json
{
  "title": "Movie 2024 BRAZILIAN-DUAL-AUDIO 1080p BluRay-SAMARITANO",
  "indexer": "Samaritano"
}
```

**Log:**
```
[RADARR-MOVIES] Applied Samaritano rules
✅ Title was modified!
  Indexer:  Samaritano
  Original: Movie 2024 MULTI 1080p BluRay
  Modified: Movie 2024 BRAZILIAN-DUAL-AUDIO 1080p BluRay-SAMARITANO
```

#### Exemplo 4: Indexer desconhecido com padrão PT-BR

**Input:**
```json
{
  "title": "Movie.2024.portuguese.1080p-GenericGroup",
  "indexer": "TrackerXYZ"
}
```

**Output:**
```json
{
  "title": "Movie 2024 portuguese 1080p.LEGENDADO-GenericGroup",
  "indexer": "TrackerXYZ"
}
```

**Log:**
```
[RADARR-MOVIES] No specific rules for TrackerXYZ, applied global rules
✅ Title was modified!
  Indexer:  TrackerXYZ
  Original: Movie.2024.portuguese.1080p-GenericGroup
  Modified: Movie 2024 portuguese 1080p.LEGENDADO-GenericGroup
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

1. **Use os nomes EXATOS dos indexers** conforme tabela acima no autobrr
2. **Use nomes descritivos em `APP_XX_NAME`** para facilitar leitura dos logs
3. **Ative DEBUG temporariamente** quando adicionar novos indexers
4. **Monitore o health check** periodicamente para detectar problemas
5. **Crie alertas** no Uptime Kuma ou similar para o endpoint `/health`
6. **Backup do docker-compose.yml** com todas as configurações
7. **Teste cada indexer individualmente** após configurar no Autobrr
8. **Verifique os logs regularmente** para identificar padrões não cobertos

---

**🎉 Pronto! Seu Autobrr agora envia títulos padronizados para os *arr apps!**