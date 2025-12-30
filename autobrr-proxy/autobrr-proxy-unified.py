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
# FUNÇÃO PARA NORMALIZAR PONTOS NO TÍTULO
# ============================================================================

def normalize_dots_in_title(title):
    """
    Substitui pontos por espaços, exceto DENTRO de padrões técnicos.
    Exemplos:
    - .H.264 → H.264 (remove ponto inicial, mantém interno)
    - .DDP5.1 → DDP5.1 (remove ponto inicial, mantém interno)
    - .x265 → x265 (remove ponto inicial)
    """
    # Remove extensão se houver (para processar e adicionar de volta depois)
    extension_match = re.search(r'\.(mkv|mp4|avi|m4v|ts|m2ts)$', title, re.IGNORECASE)
    extension = extension_match.group(0) if extension_match else ''
    if extension:
        title = title[:-len(extension)]
    
    # Padrões técnicos - SEM o ponto inicial!
    technical_patterns = [
        # Video codecs
        r'H\.26[45]',                      # H.264, H.265
        r'x26[45]',                        # x264, x265
        r'h26[45]',                        # h264, h265
        
        # Audio codecs com canais (formato compacto: DDP5.1, AAC2.0)
        r'DDP\d\.\d',                      # DDP5.1
        r'AAC\d\.\d',                      # AAC2.0
        r'DD\d\.\d',                       # DD5.1
        r'AC3\d\.\d',                      # AC35.1
        
        # Audio codecs com espaço (DD 5.1, AAC 2.0)
        r'DD[P+]?\s+\d\.\d',               # DD 5.1, DD+ 5.1, DDP 5.1
        r'AAC\s+\d\.\d',                   # AAC 2.0
        r'FLAC\s+\d\.\d',                  # FLAC 2.0
        r'AC-?3\s+\d\.\d',                 # AC3 5.1, AC-3 5.1
        r'E-?AC-?3\s+\d\.\d',              # E-AC3 5.1, EAC3 5.1
        
        # DTS variants
        r'DTS[-:]?X?\s*\d\.\d',            # DTS 5.1, DTS:X 7.1, DTS-X 7.1
        r'DTS[-\s]?HD[-\s]?MA\s*\d\.\d',   # DTS-HD MA 7.1
        r'DTS[-\s]?HD\s*\d\.\d',           # DTS-HD 5.1
        
        # TrueHD, Atmos
        r'TrueHD\s*\d\.\d',                # TrueHD 7.1
        r'Atmos\s*\d\.\d',                 # Atmos 7.1
        
        # Versões
        r'v\d+',                           # v2, v3
    ]
    
    # Adiciona ponto opcional ANTES de cada padrão para captura
    technical_patterns_with_dot = [rf'\.?{pattern}' for pattern in technical_patterns]
    
    # Temporariamente substitui padrões técnicos por placeholders
    placeholders = {}
    for i, pattern in enumerate(technical_patterns_with_dot):
        for match in re.finditer(pattern, title, re.IGNORECASE):
            placeholder = f'__TECH{i}_{len(placeholders)}__'
            # Remove o ponto inicial se existir
            original = match.group(0).lstrip('.')
            placeholders[placeholder] = original
            title = title.replace(match.group(0), placeholder)
    
    # Substitui pontos por espaços (exceto nos placeholders)
    title = title.replace('.', ' ')
    
    # Restaura padrões técnicos (agora sem ponto inicial)
    for placeholder, original in placeholders.items():
        title = title.replace(placeholder, original)
    
    # Remove espaços múltiplos
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Adiciona extensão de volta se havia
    if extension:
        title = f"{title}{extension}"
    
    return title

# ============================================================================
# REGRAS DE MODIFICAÇÃO POR INDEXER
# ============================================================================

def modify_capybarabr(title):
    """
    Regras específicas do CapybaraBR:
    - DUAL → BRAZILIAN-DUAL-AUDIO
    """
    return re.sub(r'\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title, flags=re.IGNORECASE)

def modify_brasiltracker(title):
    """
    Regras específicas do BrasilTracker:
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
    Regras específicas do Bj-Share:
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
    Regras específicas do AmigosShare:
    - dual-audio → BRAZILIAN-DUAL-AUDIO
    - dublado → DUBLADO
    - nacional → NACIONAL
    - legendado → LEGENDADO
    - Se não tiver marcador BR e não tiver grupo → adiciona -ASC
    """
    modified = title
    
    # Aplica as conversões padrão
    modified = re.sub(r'(?i)(brazilian\s+)?dual-audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?dublado', 'DUBLADO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?nacional', 'NACIONAL', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?legendado', 'LEGENDADO', modified)
    
    # Verifica se tem marcador brasileiro
    has_br_marker = re.search(
        r'(LEGENDADO|BRAZILIAN-DUAL-AUDIO|NACIONAL|DUBLADO)',
        modified,
        flags=re.IGNORECASE
    )
    
    # Verifica se tem grupo de release (-Grupo no final)
    has_release_group = re.search(r'-[A-Za-z0-9]+$', modified)
    
    # Se NÃO tem marcador brasileiro E NÃO tem grupo de release
    if not has_br_marker and not has_release_group:
        modified = f"{modified}-ASC"
    
    return modified

def modify_locadora(title):
    """
    Regras específicas do Locadora:
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
    Regras específicas do Samaritano:
    - DUAL → BRAZILIAN-DUAL-AUDIO
    - MULTI → BRAZILIAN-DUAL-AUDIO
    - -NoGroup → -SAMARITANO
    - Se não tiver grupo de release → adiciona -SAMARITANO
    """
    modified = title
    
    # Converte DUAL → BRAZILIAN-DUAL-AUDIO
    modified = re.sub(r'(?i)\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', modified)
    
    # Converte MULTI → BRAZILIAN-DUAL-AUDIO
    modified = re.sub(r'(?i)\bMULTI\b', 'BRAZILIAN-DUAL-AUDIO', modified)
    
    # Substitui NoGroup por SAMARITANO
    modified = re.sub(r'(?i)-NoGroup\b', '-SAMARITANO', modified)
    
    # Verifica se tem grupo de release (-Grupo no final)
    has_release_group = re.search(r'-[A-Za-z0-9]+$', modified)
    
    # Se NÃO tem grupo de release, adiciona -SAMARITANO
    if not has_release_group:
        modified = f"{modified}-SAMARITANO"
    
    return modified

def modify_uniotaku(title):
    """
    Regras específicas do UniOtaku:
    - Remove TODOS os colchetes [xxx]
    - Adiciona LEGENDADO antes do release group
    """
    modified = title
    
    # Remove TODOS os colchetes e o conteúdo dentro
    modified = re.sub(r'\[([^\]]+)\]', r'\1', modified)
    
    # Remove espaços múltiplos
    modified = re.sub(r'\s+', ' ', modified).strip()
    
    # Adiciona LEGENDADO antes do último "palavra" (release group)
    # Divide por espaços e adiciona LEGENDADO antes do último elemento
    parts = modified.rsplit(' ', 1)  # Separa no último espaço
    if len(parts) == 2:
        modified = f"{parts[0]} LEGENDADO {parts[1]}"
    else:
        modified = f"{modified} LEGENDADO"
    
    return modified

def modify_shakaw(title):
    """
    Regras específicas do ShaKaw:
    - Adiciona sufixo -SHAKAW no final se não existir
    """
    modified = title
    
    # Verifica se já tem -SHAKAW no final
    if not re.search(r'-SHAKAW$', modified, flags=re.IGNORECASE):
        # Adiciona -SHAKAW no final
        modified = f"{modified}-SHAKAW"
    
    return modified

def modify_global(title):
    """
    Regras globais aplicadas quando não há regra específica do indexer.
    NÃO converte DUAL genérico (pode ser idiomas não-PT em trackers gringos).
    Apenas detecta padrões EXPLICITAMENTE brasileiros.
    """
    modified = title
    
    # Detecta padrões PT-BR explícitos e adiciona LEGENDADO
    ptbr_patterns = r'(?i:\b(legendado|brazilian(-portuguese)?|brazil|portuguese|pt[-\s]?br(asil)?|port[-\s]?br|por[-\s]?br|pt[-\s]?br[-\s]sub(s)?|sub(s)?[-\s]pt[-\s]?br)\b)|\[subs?[-\[].*\bPT\b.*\]|\[subs?-\[\bPT\b[+\]]'
    
    if re.search(ptbr_patterns, modified, flags=re.IGNORECASE):
        if not re.search(r'(LEGENDADO|BRAZILIAN-DUAL-AUDIO|NACIONAL|DUBLADO|ASC|SAMARITANO)', modified, flags=re.IGNORECASE):
            # Adiciona .LEGENDADO antes do último componente (-Group)
            if re.search(r'-[A-Za-z0-9]+$', modified):
                # Tem grupo de release
                modified = re.sub(r'(-[A-Za-z0-9]+)$', r'.LEGENDADO\1', modified)
            else:
                # Não tem grupo de release
                modified = f"{modified}.LEGENDADO"
    
    return modified

# ============================================================================
# DETECÇÃO INTELIGENTE DE INDEXER
# ============================================================================

def get_indexer_function(indexer):
    """
    Detecta a função de modificação baseada no nome do indexer.
    Procura pela PALAVRA-CHAVE no nome, independente de prefixos/sufixos.
    
    Suporta formatos como:
    - torznab_amigosshare
    - newznab_capybarabr
    - prowlarr_locadora
    - CapybaraBR-trashguides
    - BrasilTracker (Prowlarr)
    """
    if not indexer:
        return None
    
    # Normaliza: lowercase, remove espaços, hífens, underscores e parênteses
    indexer_normalized = indexer.lower().replace(' ', '').replace('-', '').replace('_', '').replace('(', '').replace(')', '')
    
    # Procura por palavra-chave no nome (ordem importa! Mais específico primeiro)
    if 'capybara' in indexer_normalized or 'capybarabr' in indexer_normalized:
        return modify_capybarabr
    elif 'brasiltracker' in indexer_normalized:
        return modify_brasiltracker
    elif 'bjshare' in indexer_normalized:
        return modify_bjshare
    elif 'amigosshare' in indexer_normalized:
        return modify_amigosshare
    elif 'locadora' in indexer_normalized:
        return modify_locadora
    elif 'samaritano' in indexer_normalized:
        return modify_samaritano
    elif 'shakaw' in indexer_normalized:
        return modify_shakaw
    elif 'uniotaku' in indexer_normalized:
        return modify_uniotaku
    else:
        return None

def modify_title(title, indexer=None, app_name=None):
    """
    Aplica modificações no título baseado no indexer detectado.
    
    Fluxo:
    1. Normaliza pontos no título
    2. Detecta função de modificação baseada no indexer
    3. Aplica regras específicas ou globais
    4. Loga as mudanças
    """
    if not title:
        return title
    
    original_title = title
    
    # 1. Normaliza pontos PRIMEIRO
    title = normalize_dots_in_title(title)
    
    # 2. Detecta a função de modificação baseada no indexer
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
    
    # Log headers com valores sensíveis mascarados
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
        
        if data['title'] != original_title:
            logger.info("✅ Title was modified!")
        else:
            logger.info("ℹ️  Title unchanged")
    
    # Preparar headers
    headers = {key: value for key, value in request.headers.items() if key.lower() not in ['host', 'content-length']}
    
    if 'X-Api-Key' not in headers:
        headers['X-Api-Key'] = app_config['api_key']
        logger.info("🔑 Added API key from config")
    
    target_url = f"{app_config['url']}/{subpath}"
    
    logger.info("📤 OUTGOING REQUEST")
    logger.info(f"   Target URL: {target_url}")
    logger.info(f"   Method:     {request.method}")
    
    # Log headers de saída com valores sensíveis mascarados
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
        
        # Remover Transfer-Encoding chunked para evitar erro "bare LF"
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
    
    return jsonify({"proxy": "ok", "indexers_supported": ["capybarabr", "brasiltracker", "bjshare", "amigosshare", "locadora", "samaritano", "uniotaku"], "apps": status})

@app.route('/')
def index():
    endpoints = {}
    for app_subpath, config in APPS.items():
        display_name = f"{config['name']} ({config['type']})" if config['name'] else config['type']
        endpoints[app_subpath] = {"url": f"http://proxy:8888/{app_subpath}", "type": config['type'], "name": config['name'], "target": config['url']}
    
    return jsonify({"service": "autobrr-proxy-unified", "version": "1.1.0", "indexers_supported": ["capybarabr", "brasiltracker", "bjshare", "amigosshare", "locadora", "samaritano", "uniotaku"], "total_apps": len(APPS), "endpoints": endpoints, "log_level": LOG_LEVEL})

if __name__ == '__main__':
    if not APPS:
        logger.error("⛔ No apps configured. Exiting.")
        exit(1)
    
    logger.info("🚀 Starting Autobrr Proxy")
    logger.info(f"📊 Log Level: {LOG_LEVEL}")
    logger.info(f"🌐 Listening on: 0.0.0.0:8888")
    
    app.run(host='0.0.0.0', port=8888, debug=False)