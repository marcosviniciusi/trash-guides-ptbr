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