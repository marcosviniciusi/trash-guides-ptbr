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
# REGRAS DE MODIFICAÇÃO POR INDEXER
# ============================================================================

def modify_capybarabr(title):
    return re.sub(r'\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title, flags=re.IGNORECASE)

def modify_brasiltracker(title):
    modified = title
    modified = re.sub(r'(?i)Dual\s+Audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)\b(Subs|Legendado)\b', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)\bNacional\b', 'NACIONAL', modified)
    modified = re.sub(r'(?i)\bDublado\b', 'DUBLADO', modified)
    return re.sub(r'\s+', ' ', modified)

def modify_bjshare(title):
    modified = title
    modified = re.sub(r'Dual\s+[\x80-\xFF]udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'Dual\s+.udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)Legendado', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)Nacional', 'NACIONAL', modified)
    return re.sub(r'\s{2,}', ' ', modified)

def modify_amigosshare(title):
    modified = title
    modified = re.sub(r'(?i)(brazilian\s+)?dual-audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?dublado', 'DUBLADO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?nacional', 'NACIONAL', modified)
    return re.sub(r'(?i)(brazilian\s+)?legendado', 'LEGENDADO', modified)

def modify_locadora(title):
    modified = title
    modified = re.sub(r'(?i)\bDUAL-', 'BRAZILIAN-DUAL-AUDIO-', modified)
    modified = re.sub(r'(?i)\s*/\s*Portuguese\s*\([^)]*\)\s+\w+.*$', '', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*Portuguese\s*\([^)]*\)\s*$', r'NACIONAL-\1', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*(?!Portuguese)[A-Za-z].*$', r'LEGENDADO-\1', modified)
    return re.sub(r'(?i)-JPN', '', modified)

def modify_samaritano(title):
    return re.sub(r'(?i)\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title)

INDEXER_RULES = {
    'capybarabr': modify_capybarabr,
    'brasiltracker': modify_brasiltracker,
    'bjshare': modify_bjshare,
    'bj-share': modify_bjshare,
    'amigosshare': modify_amigosshare,
    'amigos-share': modify_amigosshare,
    'locadora': modify_locadora,
    'samaritano': modify_samaritano,
}

def modify_global(title):
    modified = title
    modified = re.sub(r'\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', modified, flags=re.IGNORECASE)
    modified = re.sub(r'\bPT-BR\b', 'BRAZILIAN', modified, flags=re.IGNORECASE)
    return re.sub(r'\bPortuguese\b', 'BRAZILIAN', modified, flags=re.IGNORECASE)

def modify_title(title, indexer=None, app_name=None):
    if not title:
        return title
    
    original_title = title
    indexer_key = indexer.lower().replace(' ', '').replace('-', '') if indexer else None
    
    if indexer_key and indexer_key in INDEXER_RULES:
        modified = INDEXER_RULES[indexer_key](title)
        logger.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] Applied {indexer} rules")
    else:
        modified = modify_global(title)
        if indexer:
            logger.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] No specific rules for {indexer}")
    
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
    
    return jsonify({"proxy": "ok", "indexers_supported": list(INDEXER_RULES.keys()), "apps": status})

@app.route('/')
def index():
    endpoints = {}
    for app_subpath, config in APPS.items():
        display_name = f"{config['name']} ({config['type']})" if config['name'] else config['type']
        endpoints[app_subpath] = {"url": f"http://proxy:8888/{app_subpath}", "type": config['type'], "name": config['name'], "target": config['url']}
    
    return jsonify({"service": "autobrr-proxy-unified", "version": "1.0.7", "indexers_supported": list(INDEXER_RULES.keys()), "total_apps": len(APPS), "endpoints": endpoints, "log_level": LOG_LEVEL})

if __name__ == '__main__':
    if not APPS:
        logger.error("⛔ No apps configured. Exiting.")
        exit(1)
    
    logger.info("🚀 Starting Autobrr Proxy")
    logger.info(f"📊 Log Level: {LOG_LEVEL}")
    logger.info(f"🌐 Listening on: 0.0.0.0:8888")
    
    app.run(host='0.0.0.0', port=8888, debug=False)