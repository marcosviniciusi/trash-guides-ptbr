#!/bin/bash

BASE_URL="https://github.com/marcosviniciusi/trash-guides-ptbr/releases/latest/download"

mkdir -p custom_formats

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

# Custom Formats - Idioma PT-BR
download_format 'custom-brazilian-group-tier-dual-audio.json'
download_format 'custom-brazilian-dual-language.json'
download_format 'custom-brazilian-group-tier-subtitles.json'
download_format 'custom-brazilian-subtitles.json'
download_format 'custom-brazilian-group-tier-dubbed.json'
download_format 'custom-brazilian-dubbed.json'
download_format 'custom-original-language.json'
download_format 'custom-brazilian-group-tier-bad.json'
download_format 'custom-us-group-tier-premium.json'

# Custom Formats - Plataformas
download_format 'sonarr-custom-pt-br-globoplay.json'
download_format 'radarr-custom-pt-br-globoplay.json'

# Custom Formats - Codec
download_format 'radarr-custom-pt-br-x264.json'
download_format 'radarr-custom-pt-br-x265.json'
download_format 'radarr-custom-pt-br-h264.json'
download_format 'radarr-custom-pt-br-h265.json'
download_format 'sonarr-custom-pt-br-x264.json'
download_format 'sonarr-custom-pt-br-x265.json'
download_format 'sonarr-custom-pt-br-h264.json'
download_format 'sonarr-custom-pt-br-h265.json'

# Custom Formats - Season Pack
download_format 'sonarr-custom-season-pack.json'

# Custom Formats - Release Quality (Radarr)
download_format 'radarr-uhd-remux-release.json'
download_format 'radarr-fhd-remux-release.json'
download_format 'radarr-hd-remux-release.json'
download_format 'radarr-uhd-bluray-release.json'
download_format 'radarr-fhd-bluray-release.json'
download_format 'radarr-hd-bluray-release.json'
download_format 'radarr-uhd-web-release.json'
download_format 'radarr-fhd-web-release.json'
download_format 'radarr-hd-web-release.json'

# Custom Formats - Release Quality (Sonarr)
download_format 'sonarr-uhd-remux-release.json'
download_format 'sonarr-fhd-remux-release.json'
download_format 'sonarr-hd-remux-release.json'
download_format 'sonarr-uhd-bluray-release.json'
download_format 'sonarr-fhd-bluray-release.json'
download_format 'sonarr-hd-bluray-release.json'
download_format 'sonarr-uhd-web-release.json'
download_format 'sonarr-fhd-web-release.json'
download_format 'sonarr-hd-web-release.json'

echo "✅ Custom formats baixados com sucesso!"
