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

echo "✅ Custom formats baixados com sucesso!"