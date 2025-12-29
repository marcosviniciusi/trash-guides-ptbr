#!/usr/bin/env python3
# autobrr-proxy-unified.py

from flask import Flask, request, jsonify
import requests
import re
import logging
import os

app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

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
    """
    Carrega apps dinamicamente das variáveis de ambiente usando padrão de ID.
    
    Formato esperado das variáveis:
    APP_<ID>_TYPE=radarr|sonarr|lidarr|readarr|whisparr
    APP_<ID>_NAME=Movies|Anime|4K|Series (opcional)
    APP_<ID>_SUBPATH=radarr-movies|radarr-anime|sonarr-4k
    APP_<ID>_URL=http://radarr:7878
    APP_<ID>_API_KEY=abc123xyz
    """
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
            logging.warning(
                f"⚠️  APP_{app_id}: Incomplete configuration. "
                f"Need TYPE, SUBPATH, URL, and API_KEY. Skipping."
            )
            continue
        
        valid_types = ['radarr', 'sonarr', 'lidarr', 'readarr', 'whisparr']
        if app_type.lower() not in valid_types:
            logging.warning(
                f"⚠️  APP_{app_id}: Invalid TYPE '{app_type}'. "
                f"Must be one of: {', '.join(valid_types)}. Skipping."
            )
            continue
        
        apps[subpath] = {
            'id': app_id,
            'type': app_type.lower(),
            'name': name,
            'url': url.rstrip('/'),
            'api_key': api_key,
        }
        
        display_name = f"{name} ({app_type})" if name else app_type
        logging.info(
            f"✅ APP_{app_id}: {display_name} → /{subpath} → {url}"
        )
    
    if not apps:
        logging.error("❌ No apps configured! Check your environment variables.")
        logging.error("Expected format: APP_01_TYPE, APP_01_SUBPATH, APP_01_URL, APP_01_API_KEY")
    else:
        logging.info(f"✅ Total apps loaded: {len(apps)}")
        logging.info(f"Available endpoints: {', '.join([f'/{k}' for k in apps.keys()])}")
    
    return apps

APPS = load_apps_from_env()

# ============================================================================
# REGRAS DE MODIFICAÇÃO POR INDEXER
# ============================================================================

def modify_capybarabr(title):
    modified = re.sub(r'\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title, flags=re.IGNORECASE)
    return modified

def modify_brasiltracker(title):
    modified = title
    modified = re.sub(r'(?i)Dual\s+Audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)\b(Subs|Legendado)\b', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)\bNacional\b', 'NACIONAL', modified)
    modified = re.sub(r'(?i)\bDublado\b', 'DUBLADO', modified)
    modified = re.sub(r'\s+', ' ', modified)
    return modified

def modify_bjshare(title):
    modified = title
    modified = re.sub(r'Dual\s+[\x80-\xFF]udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'Dual\s+.udio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)Legendado', 'LEGENDADO', modified)
    modified = re.sub(r'(?i)Nacional', 'NACIONAL', modified)
    modified = re.sub(r'\s{2,}', ' ', modified)
    return modified

def modify_amigosshare(title):
    modified = title
    modified = re.sub(r'(?i)(brazilian\s+)?dual-audio', 'BRAZILIAN-DUAL-AUDIO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?dublado', 'DUBLADO', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?nacional', 'NACIONAL', modified)
    modified = re.sub(r'(?i)(brazilian\s+)?legendado', 'LEGENDADO', modified)
    return modified

def modify_locadora(title):
    modified = title
    modified = re.sub(r'(?i)\bDUAL-', 'BRAZILIAN-DUAL-AUDIO-', modified)
    modified = re.sub(r'(?i)\s*/\s*Portuguese\s*\([^)]*\)\s+\w+.*$', '', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*Portuguese\s*\([^)]*\)\s*$', r'NACIONAL-\1', modified)
    modified = re.sub(r'(?i)(\S+)\s*/\s*(?!Portuguese)[A-Za-z].*$', r'LEGENDADO-\1', modified)
    modified = re.sub(r'(?i)-JPN', '', modified)
    return modified

def modify_samaritano(title):
    modified = re.sub(r'(?i)\bDUAL\b', 'BRAZILIAN-DUAL-AUDIO', title)
    return modified

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
    modified = re.sub(r'\bPortuguese\b', 'BRAZILIAN', modified, flags=re.IGNORECASE)
    return modified

def modify_title(title, indexer=None, app_name=None):
    if not title:
        return title
    
    original_title = title
    indexer_key = indexer.lower().replace(' ', '').replace('-', '') if indexer else None
    
    if indexer_key and indexer_key in INDEXER_RULES:
        modified = INDEXER_RULES[indexer_key](title)
        logging.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] Applied {indexer} rules")
    else:
        modified = modify_global(title)
        if indexer:
            logging.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] No specific rules for {indexer}, applied global rules")
    
    if modified != original_title:
        logging.info(f"[{app_name.upper() if app_name else 'UNKNOWN'}] Title modified:")
        logging.info(f"  Indexer:  {indexer if indexer else 'unknown'}")
        logging.info(f"  Original: {original_title}")
        logging.info(f"  Modified: {modified}")
    
    return modified

# ============================================================================
# PROXY HANDLER
# ============================================================================

def proxy_request(app_subpath, subpath):
    if app_subpath not in APPS:
        return jsonify({
            "error": f"Unknown endpoint: /{app_subpath}",
            "available_endpoints": list(APPS.keys())
        }), 404
    
    app_config = APPS[app_subpath]
    data = request.get_json() if request.is_json else None
    
    app_display = f"{app_config['name']} ({app_config['type']})" if app_config['name'] else app_config['type']
    logging.info(f"[{app_subpath.upper()}] {app_display} - Received {request.method} /{subpath}")
    
    # ✅ CORRIGIDO: Verifica múltiplos endpoints
    if subpath in RELEASE_PUSH_ENDPOINTS and data:
        if 'title' in data:
            indexer = data.get('indexer', data.get('indexerName', None))
            data['title'] = modify_title(data['title'], indexer, app_subpath)
    
    headers = dict(request.headers)
    headers.pop('Host', None)
    headers.pop('Content-Length', None)
    
    if 'X-Api-Key' not in headers:
        headers['X-Api-Key'] = app_config['api_key']
    
    target_url = f"{app_config['url']}/{subpath}"
    
    try:
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            json=data,
            params=request.args,
            timeout=30,
            allow_redirects=False
        )
        
        logging.info(f"[{app_subpath.upper()}] → {app_config['url']}: {response.status_code}")
        return response.content, response.status_code, dict(response.headers.items())
        
    except requests.exceptions.RequestException as e:
        logging.error(f"[{app_subpath.upper()}] Error: {e}")
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
        # ✅ CORRIGIDO: Health check usa endpoint correto por tipo
        if config['type'] in ['radarr', 'sonarr', 'whisparr']:
            health_endpoint = 'api/v3/system/status'
        elif config['type'] in ['lidarr', 'readarr']:
            health_endpoint = 'api/v1/system/status'
        else:
            health_endpoint = 'api/v3/system/status'
        
        try:
            r = requests.get(
                f"{config['url']}/{health_endpoint}",
                headers={'X-Api-Key': config['api_key']},
                timeout=5
            )
            status[app_subpath] = {
                "status": "ok" if r.status_code == 200 else "error",
                "type": config['type'],
                "name": config['name'],
                "url": config['url']
            }
        except Exception as e:
            status[app_subpath] = {
                "status": "unreachable",
                "type": config['type'],
                "name": config['name'],
                "url": config['url'],
                "error": str(e)
            }
    
    return jsonify({
        "proxy": "ok",
        "indexers_supported": list(INDEXER_RULES.keys()),
        "apps": status
    })

@app.route('/')
def index():
    endpoints = {}
    for app_subpath, config in APPS.items():
        display_name = f"{config['name']} ({config['type']})" if config['name'] else config['type']
        endpoints[app_subpath] = {
            "url": f"http://proxy:8888/{app_subpath}",
            "type": config['type'],
            "name": config['name'],
            "target": config['url']
        }
    
    return jsonify({
        "service": "autobrr-proxy-unified",
        "version": "2.0.1",
        "indexers_supported": list(INDEXER_RULES.keys()),
        "total_apps": len(APPS),
        "endpoints": endpoints
    })

if __name__ == '__main__':
    if not APPS:
        logging.error("⛔ No apps configured. Exiting.")
        exit(1)
    
    app.run(host='0.0.0.0', port=8888, debug=False)