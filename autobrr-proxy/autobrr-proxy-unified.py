#!/usr/bin/env python3
# autobrr-proxy-unified.py

from flask import Flask, request, jsonify
import requests
import re
import logging
import os
import json

app = Flask(__name__)

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# ============================================================================
# FUNÇÃO PARA MASCARAR VALORES SENSÍVEIS
# ============================================================================

def mask_sensitive_value(header, value):
    """Mascara valores sensíveis baseado no nome do header"""
    sensitive_headers = ['x-api-key', 'authorization', 'api-key', 'token', 'password', 'secret']
    
    if any(sensitive in header.lower() for sensitive in sensitive_headers):
        if not value or len(value) < 12:
            return "***"
        return f"{value[:8]}...{value[-4:]}"
    
    return value

# ============================================================================
# ENDPOINTS DE RELEASE PUSH (MÚLTIPLAS VERSÕES)
# ============================================================================

RELEASE_PUSH_ENDPOINTS = [
    'api/v1/release/push',  # Lidarr, Readarr
    'api/v3/release/push',  # Radarr, Sonarr, Whisparr
]

# ============================================================================
# CONFIGURAÇÃO DINÂMICA DOS *ARR APPS
# ============================================================================

def load_apps_from_env():
    """Carrega apps dinamicamente das variáveis de ambiente"""
    apps = {}
    
    for i in range(1, 100):
        app_id = f"{i:02d}"
        
        app_type = os.getenv(f'APP_{app_id}_TYPE')
        subpath = os.getenv(f'APP_{app_id}_SUBPATH')
        url = os.getenv(f'APP_{app_id}_URL')
        api_key = os.getenv(f'APP_{app_id}_API_KEY')
        name = os.getenv(f'APP_{app_id}_NAME', '')
        
        if not app_type:
            if apps and i < 20:
                continue
            else:
                break
        
        if not all([app_type, subpath, url, api_key]):
            logger.warning(f"⚠️  APP_{app_id}: Incomplete configuration.")
            continue
        
        valid_types = ['radarr', 'sonarr', 'lidarr', 'readarr', 'whisparr']
        if app_type.lower() not in valid_types:
            logger.warning(f"⚠️  APP_{app_id}: Invalid TYPE '{app_type}'.")
            continue
        
        apps[subpath] = {
            'id': app_id,
            'type': app_type.lower(),
            'name': name,
            'url': url.rstrip('/'),
            'api_key': api_key,
        }
        
        display_name = f"{name} ({app_type})" if name else app_type
        logger.info(f"✅ APP_{app_id}: {display_name} → /{subpath} → {url}")
    
    if not apps:
        logger.error("❌ No apps configured!")
    else:
        logger.info(f"✅ Total apps loaded: {len(apps)}")
    
    return apps

APPS = load_apps_from_env()

# ============================================================================
# HELPER: Detecta se tem grupo de release
# ============================================================================

def has_release_group(title):
    """
    Detecta se o título tem grupo de release no final.
    
    Grupo válido:
    - Termina com -XXX (mínimo 2 caracteres alfanuméricos)
    - NÃO é -DL (parte de WEB-DL)
    
    Exemplos:
    - Movie 2024 WEB-DL → False (sem grupo)
    - Movie 2024 WEB-DL-Group → True (tem grupo)
    - Movie 2024-YG → True (grupo de 2 chars)
    """
    match = re.search(r'-([A-Za-z0-9]{2,})$', title)
    
    if not match:
        return False
    
    group_name = match.group(1).upper()
    
    # Exclui apenas -DL (parte de WEB-DL)
    return group_name != 'DL'

# ============================================================================
# FUNÇÃO PARA NORMALIZAR PONTOS NO TÍTULO
# ============================================================================

def normalize_dots_in_title(title):
    """
    Substitui pontos por espaços, exceto DENTRO de padrões técnicos.
    """
    # Remove extensão se houver
    extension_match = re.search(r'\.(mkv|mp4|avi|m4v|ts|m2ts)$', title, re.IGNORECASE)
    extension = extension_match.group(0) if extension_match else ''
    if extension:
        title = title[:-len(extension)]
    
    # Padrões técnicos (SEM ponto inicial)
    technical_patterns = [
        r'H\.26[45]',
        r'x26[45]',
        r'h26[45]',
        r'DDP\d\.\d',
        r'AAC\d\.\d',
        r'DD\d\.\d',
        r'AC3\d\.\d',
        r'DD[P+]?\s+\d\.\d',
        r'AAC\s+\d\.\d',
        r'FLAC\s+\d\.\d',
        r'AC-?3\s+\d\.\d',
        r'E-?AC-?3\s+\d\.\d',
        r'DTS[-:]?X?\s*\d\.\d',
        r'DTS[-\s]?HD[-\s]?MA\s*\d\.\d',
        r'DTS[-\s]?HD\s*\d\.\d',
        r'TrueHD\s*\d\.\d',
        r'Atmos\s*\d\.\d',
        r'v\d+',
    ]
    
    # Adiciona ponto opcional antes de cada padrão
    technical_patterns_with_dot = [rf'\.?{pattern}' for pattern in technical_patterns]
    
    # Substitui por placeholders
    placeholders = {}
    for i, pattern in enumerate(technical_patterns_with_dot):
        for match in re.finditer(pattern, title, re.IGNORECASE):
            placeholder = f'__TECH{i}_{len(placeholders)}__'
            original = match.group(0).lstrip('.')
            placeholders[placeholder] = original
            title = title.replace(match.group(0), placeholder)
    
    # Substitui pontos por espaços
    title = title.replace('.', ' ')
    
    # Restaura padrões técnicos
    for placeholder, original in placeholders.items():
        title = title.replace(placeholder, original)
    
    # Remove espaços múltiplos
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Adiciona extensão de volta
    if extension:
        title = f"{title}{extension}"
    
    return title

# ============================================================================
# REGRAS DE MODIFICAÇÃO POR INDEXER
# ============================================================================

def modify_capybarabr(title):
    """
    CapybaraBR:
    - DUAL → BRAZILIAN-DUAL-AUDIO
    """
    return re.sub(r'\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title, flags=re.IGNORECASE)

def modify_brasiltracker(title):
    """
    BrasilTracker:
    - Dual Audio → BRAZILIAN-DUAL-AUDIO
    - Subs/Legendado → LEGENDADO
    - Nacional → NACIONAL
    - Dublado → DUBLADO
    """
    modified = title
    modified = re.sub(r'(?i)Dual\s+Audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)\b(Subs|Legendado)\b', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)\bNacional\b', 'NACIONAL', modified)
    modified = re.sub(r'(?i)\bDublado\b', 'DUBLADO', modified)
    return re.sub(r'\s+', ' ', modified)

def modify_bjshare(title):
    """
    Bj-Share:
    - Dual Áudio → BRAZILIAN-DUAL-AUDIO
    - Legendado → LEGENDADO
    - Nacional → NACIONAL
    """
    modified = title
    modified = re.sub(r'Dual\s+[\x80-\xFF]udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'Dual\s+.udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)Legendado', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)Nacional', 'NACIONAL', modified)
    return re.sub(r'\s{2,}', ' ', modified)

def modify_amigosshare(title):
    """
    AmigosShare:
    - dual-audio → BRAZILIAN-DUAL-AUDIO
    - dublado → DUBLADO
    - nacional → NACIONAL
    - legendado → LEGENDADO
    - Sem marcador BR + sem grupo → adiciona -ASC
    """
    modified = title
    
    # Conversões
    modified = re.sub(r'(?i)(brazilian\s+)?dual-audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?dublado', 'DUBLADO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?nacional', 'NACIONAL', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?legendado', 'LEGENDADO', modified)
    
    # Verifica marcador BR
    has_br_marker = re.search(
        r'(LEGENDADO|BRAZILIAN-DUAL-AUDIO|NACIONAL|DUBLADO)',
        modified,
        flags=re.IGNORECASE
    )
    
    # Se NÃO tem marcador BR E NÃO tem grupo → adiciona -ASC
    if not has_br_marker and not has_release_group(modified):
        modified = f"{modified}-ASC"
    
    return modified

def modify_locadora(title):
    """
    Locadora:
    - Remove sufixos: / Language (Code)
    - DUAL- → BRAZILIAN-DUAL-AUDIO-
    - Adiciona LEGENDADO para idiomas não-PT
    - Remove -JPN
    """
    modified = title
    modified = re.sub(r'(?i)\bDUAL-', 'BRAZILIAN-DUAL-AUDIO-', modified)
    modified = re.sub(r'(?i)\s*/\s*Portuguese\s*\([^)]*\)\s+\w+.*$', '', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*Portuguese\s*\([^)]*\)\s*$', r'NACIONAL-\1', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*(?!Portuguese)[A-Za-z].*$', r'LEGENDADO-\1', modified)
    return re.sub(r'(?i)-JPN', '', modified)

def modify_samaritano(title):
    """
    Samaritano:
    - DUAL → BRAZILIAN-DUAL-AUDIO
    - MULTI → BRAZILIAN-DUAL-AUDIO
    - -NoGroup → -SAMARITANO
    - Sem grupo → adiciona -SAMARITANO
    """
    modified = title
    
    # Conversões
    modified = re.sub(r'(?i)\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)\bMULTI\b', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)-NoGroup\b', '-SAMARITANO', modified)
    
    # Se NÃO tem grupo → adiciona -SAMARITANO
    if not has_release_group(modified):
        modified = f"{modified}-SAMARITANO"
    
    return modified

def modify_shakaw(title):
    """
    ShaKaw:
    - Adiciona sufixo -SHAKAW se não existir
    """
    if not re.search(r'-SHAKAW$', title, flags=re.IGNORECASE):
        return f"{title}-SHAKAW"
    return title

def modify_uniotaku(title):
    """
    UniOtaku:
    - Remove TODOS os colchetes [xxx]
    - Adiciona LEGENDADO antes do último elemento
    """
    # Remove colchetes
    modified = re.sub(r'\[([^\]]+)\]', r'\1', title)
    modified = re.sub(r'\s+', ' ', modified).strip()
    
    # Adiciona LEGENDADO antes do último elemento
    parts = modified.rsplit(' ', 1)
    if len(parts) == 2:
        modified = f"{parts[0]} LEGENDADO {parts[1]}"
    else:
        modified = f"{modified} LEGENDADO"
    
    return modified

def modify_global(title):
    """
    Regras globais para indexers desconhecidos.
    Detecta padrões PT-BR explícitos e adiciona LEGENDADO.
    """
    modified = title
    
    ptbr_patterns = r'(?i:\b(legendado|brazilian(-portuguese)?|brazil|portuguese|pt[-\s]?br(asil)?|port[-\s]?br|por[-\s]?br|pt[-\s]?br[-\s]sub(s)?|sub(s)?[-\s]pt[-\s]?br)\b)|\[subs?[-\[].*\bPT\b.*\]|\[subs?-\[\bPT\b[+\]]'
    
    if re.search(ptbr_patterns, modified, flags=re.IGNORECASE):
        if not re.search(r'(LEGENDADO|BRAZILIAN-DUAL-AUDIO|NACIONAL|DUBLADO|ASC|SAMARITANO|SHAKAW)', modified, flags=re.IGNORECASE):
            if has_release_group(modified):
                # Tem grupo: adiciona .LEGENDADO antes do grupo
                modified = re.sub(r'(-[A-Za-z0-9]{2,})$', r'.LEGENDADO\1', modified)
            else:
                # Sem grupo: adiciona .LEGENDADO no final
                modified = f"{modified}.LEGENDADO"
    
    return modified

# ============================================================================
# DETECÇÃO INTELIGENTE DE INDEXER
# ============================================================================

def get_indexer_function(indexer):
    """
    Detecta a função de modificação baseada no nome do indexer.
    Procura pela palavra-chave, independente de prefixos/sufixos.
    """
    if not indexer:
        return None
    
    # Normaliza
    indexer_normalized = indexer.lower().replace(' ', '').replace('-', '').replace('_', '').replace('(', '').replace(')', '')
    
    # Detecção (ordem importa!)
    if 'capybara' in indexer_normalized or 'capybarabr' in indexer_normalized:
        return modify_capybarabr
    elif 'brasiltracker' in indexer_normalized:
        return modify_brasiltracker
    elif 'bjshare' in indexer_normalized:
        return modify_bjshare
    elif 'amigosshare' in indexer_normalized or 'amigos' in indexer_normalized:
        return modify_amigosshare
    elif 'locadora' in indexer_normalized:
        return modify_locadora
    elif 'samaritano' in indexer_normalized:
        return modify_samaritano
    elif 'shakaw' in indexer_normalized:
        return modify_shakaw
    elif 'uniotaku' in indexer_normalized or 'otaku' in indexer_normalized:
        return modify_uniotaku
    else:
        return None

def modify_title(title, indexer=None, app_name=None):
    """
    Aplica modificações no título baseado no indexer detectado.
    
    Fluxo:
    1. Normaliza pontos
    2. Detecta e aplica regras específicas ou globais
    3. Loga mudanças
    """
    if not title:
        return title
    
    original_title = title
    
    # 1. Normaliza pontos PRIMEIRO
    title = normalize_dots_in_title(title)
    
    # 2. Detecta função de modificação
    modify_func = get_indexer_function(indexer)
    
    if modify_func:
        modified = modify_func(title)
        logger.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] Applied {indexer} rules")
    else:
        modified = modify_global(title)
        if indexer:
            logger.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] No specific rules for {indexer}, applied global rules")
    
    if modified != original_title:
        logger.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] Title modified:")
        logger.info(f"  Indexer:  {indexer if indexer else 'unknown'}")
        logger.info(f"  Original: {original_title}")
        logger.info(f"  Modified: {modified}")
    else:
        logger.info(f"ℹ️  Title unchanged")
    
    return modified

# ============================================================================
# PROXY HANDLER
# ============================================================================

def proxy_request(app_subpath, subpath):
    if app_subpath not in APPS:
        return jsonify({"error": f"Unknown endpoint: /{app_subpath}"}), 404
    
    app_config = APPS[app_subpath]
    app_display = f"{app_config['name']} ({app_config['type']})" if app_config['name'] else app_config['type']
    
    logger.info("=" * 80)
    logger.info(f"📥 INCOMING REQUEST")
    logger.info(f"   App:      {app_display}")
    logger.info(f"   Endpoint: /{app_subpath}/{subpath}")
    logger.info(f"   Method:   {request.method}")
    logger.info(f"   From IP:  {request.remote_addr}")
    
    logger.info("📋 Request Headers:")
    for header, value in request.headers.items():
        masked_value = mask_sensitive_value(header, value)
        logger.info(f"   {header}: {masked_value}")
    
    data = request.get_json(silent=True) if request.is_json else None
    
    if data:
        logger.info("📦 Request Payload:")
        try:
            for line in json.dumps(data, indent=2, ensure_ascii=False).split('\n'):
                logger.info(f"   {line}")
        except:
            logger.info(f"   {data}")
    else:
        logger.info("📦 No JSON payload")
    
    if request.args:
        logger.info("🔍 Query Parameters:")
        for key, value in request.args.items():
            logger.info(f"   {key}={value}")
    
    # Modificação do título
    if subpath in RELEASE_PUSH_ENDPOINTS and data and 'title' in data:
        indexer = data.get('indexer', data.get('indexerName'))
        original_title = data['title']
        
        logger.info("🔧 Processing title modification...")
        data['title'] = modify_title(data['title'], indexer, app_subpath)
    
    # Preparar headers
    headers = {key: value for key, value in request.headers.items() if key.lower() not in ['host', 'content-length']}
    
    if 'X-Api-Key' not in headers:
        headers['X-Api-Key'] = app_config['api_key']
        logger.info("🔑 Added API key from config")
    
    target_url = f"{app_config['url']}/{subpath}"
    
    logger.info("📤 OUTGOING REQUEST")
    logger.info(f"   Target URL: {target_url}")
    logger.info(f"   Method:     {request.method}")
    
    logger.info("📋 Outgoing Headers:")
    for header, value in headers.items():
        masked_value = mask_sensitive_value(header, value)
        logger.info(f"   {header}: {masked_value}")
    
    if data:
        logger.info("📦 Payload being sent:")
        try:
            for line in json.dumps(data, indent=2, ensure_ascii=False).split('\n'):
                logger.info(f"   {line}")
        except:
            logger.info(f"   {data}")
    
    # Executar request
    try:
        logger.info(f"⏳ Sending request to {app_config['type']}...")
        
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            json=data,
            params=request.args,
            timeout=30,
            allow_redirects=False
        )
        
        logger.info("📨 RESPONSE RECEIVED")
        logger.info(f"   Status Code: {response.status_code}")
        logger.info(f"   Status:      {response.reason}")
        
        logger.info("📋 Response Headers:")
        for header, value in response.headers.items():
            logger.info(f"   {header}: {value}")
        
        if response.headers.get('Content-Type', '').startswith('application/json'):
            try:
                response_json = response.json()
                logger.info("📦 Response Body:")
                for line in json.dumps(response_json, indent=2, ensure_ascii=False).split('\n')[:20]:
                    logger.info(f"   {line}")
            except:
                logger.info(f"   Body: {response.text[:200]}")
        
        if 200 <= response.status_code < 300:
            logger.info(f"✅ SUCCESS")
        elif response.status_code >= 400:
            logger.warning(f"⚠️  WARNING - Error status")
        
        logger.info("=" * 80)
        
        # Remover Transfer-Encoding chunked
        response_headers = dict(response.headers.items())
        response_headers.pop('Transfer-Encoding', None)
        response_headers.pop('Content-Length', None)
        
        content = response.content
        if response.headers.get('Content-Encoding') == 'gzip':
            response_headers.pop('Content-Encoding', None)
        
        response_headers['Content-Length'] = str(len(content))
        
        return content, response.status_code, response_headers
        
    except requests.exceptions.Timeout:
        logger.error(f"⏱️  TIMEOUT")
        logger.error("=" * 80)
        return jsonify({"error": "Timeout"}), 504
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"🔌 CONNECTION ERROR")
        logger.error(f"   Error: {str(e)}")
        logger.error("=" * 80)
        return jsonify({"error": str(e)}), 502
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ REQUEST ERROR: {str(e)}")
        logger.error("=" * 80)
        return jsonify({"error": str(e)}), 502

# ============================================================================
# ROTAS DINÂMICAS
# ============================================================================

def create_routes():
    for app_subpath in APPS.keys():
        app.add_url_rule(
            f'/{app_subpath}',
            f'proxy_{app_subpath}_base',
            lambda asp=app_subpath: proxy_request(asp, ''),
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )
        
        app.add_url_rule(
            f'/{app_subpath}/<path:subpath>',
            f'proxy_{app_subpath}',
            lambda subpath, asp=app_subpath: proxy_request(asp, subpath),
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

create_routes()

# ============================================================================
# ROTAS DE UTILIDADE
# ============================================================================

@app.route('/health')
def health():
    status = {}
    for app_subpath, config in APPS.items():
        health_endpoint = 'api/v3/system/status' if config['type'] in ['radarr', 'sonarr', 'whisparr'] else 'api/v1/system/status'
        
        try:
            r = requests.get(f"{config['url']}/{health_endpoint}", headers={'X-Api-Key': config['api_key']}, timeout=5)
            status[app_subpath] = {"status": "ok" if r.status_code == 200 else "error", "type": config['type'], "name": config['name'], "url": config['url']}
        except Exception as e:
            status[app_subpath] = {"status": "unreachable", "type": config['type'], "name": config['name'], "url": config['url'], "error": str(e)}
    
    return jsonify({"proxy": "ok", "indexers_supported": ["capybarabr", "brasiltracker", "bjshare", "amigosshare", "locadora", "samaritano", "shakaw", "uniotaku"], "apps": status})

@app.route('/')
def index():
    endpoints = {}
    for app_subpath, config in APPS.items():
        display_name = f"{config['name']} ({config['type']})" if config['name'] else config['type']
        endpoints[app_subpath] = {"url": f"http://proxy:8888/{app_subpath}", "type": config['type'], "name": config['name'], "target": config['url']}
    
    return jsonify({"service": "autobrr-proxy-unified", "version": "1.1.0", "indexers_supported": ["capybarabr", "brasiltracker", "bjshare", "amigosshare", "locadora", "samaritano", "shakaw", "uniotaku"], "total_apps": len(APPS), "endpoints": endpoints, "log_level": LOG_LEVEL})

if __name__ == '__main__':
    if not APPS:
        logger.error("⛔ No apps configured. Exiting.")
        exit(1)
    
    logger.info("🚀 Starting Autobrr Proxy")
    logger.info(f"📊 Log Level: {LOG_LEVEL}")
    logger.info(f"🌐 Listening on: 0.0.0.0:8888")
    
    app.run(host='0.0.0.0', port=8888, debug=False)