# TRaSH Guides PT-BR - Custom Formats

Custom Formats otimizados para conteúdo em Português Brasileiro, compatível com Recyclarr e TRaSH Guides.

## 📁 Estrutura do Repositório

```
trash-guides-ptbr/
├── custom-formats/
│   ├── custom-web-tier-ptbr-dual.json
│   ├── custom-web-tier-ptbr-not-dual.json
│   ├── custom-web-tier-ptbr-not-group-radarr.json
│   └── custom-web-tier-ptbr-not-group-sonarr.json
├── recyclarr/
│   └── recyclarr.yaml
└── readme.md
```

## 🎯 Custom Formats Disponíveis

### Para Radarr e Sonarr
- **custom-web-tier-ptbr-dual** - Releases DUAL (PT-BR + Original)
- **custom-web-tier-ptbr-not-dual** - Releases apenas PT-BR (legendados)
- **custom-web-tier-ptbr-not-group-radarr** - Releases não conhecidos com audio e/ou legenda em Portugues (Radarr) ( Legendado )
- **custom-web-tier-ptbr-not-group-sonarr** - Releases não conhecidos com audio e/ou legenda em Portugues (Sonarr) ( Legendado )

## ⚙️ Configuração no Recyclarr

### Radarr - Exemplo De um arquivo apenas com estes releases ( se caso não quiser com o Trash-Guides )

```yaml
# recyclarr.yaml

radarr:
  movies:
    base_url: http://radarr:7878
    api_key: !env RADARR_API_KEY
    
    quality_profiles:
      - name: HD
    
    custom_formats:
      # Custom Format: DUAL (Prioridade máxima)
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-dual
        quality_profiles:
          - name: HD
            score: 6000

      # Custom Format: Legendado (Prioridade alta)
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-dual
        quality_profiles:
          - name: HD
            score: 5500

      # Custom Format: Filtro de grupos
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-group-radarr
        quality_profiles:
          - name: HD
            score: 5200
```

### Sonarr - Exemplo De um arquivo apenas com estes releases ( se caso não quiser com o Trash-Guides )

```yaml
sonarr:
  series:
    base_url: http://sonarr:8989
    api_key: !env SONARR_API_KEY
    
    quality_profiles:
      - name: HD
    
    custom_formats:
      # Custom Format: DUAL (Prioridade máxima)
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-dual
        quality_profiles:
          - name: HD
            score: 6000

      # Custom Format: Legendado (Prioridade alta)
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-dual
        quality_profiles:
          - name: HD
            score: 5500

      # Custom Format: Filtro de grupos
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-group-sonarr
        quality_profiles:
          - name: HD
            score: 5200
```

## 📊 Scores Recomendados

| Custom Format | Score | Descrição |
|---------------|-------|-----------|
| DUAL | 6000 | Prioridade máxima - Áudio PT-BR + Original |
| Not-DUAL | 5500 | Prioridade alta - Apenas legendas PT-BR |
| Not-GROUP| 5200 | Releases não conhecidos com audio e/ou legenda em Portugues |

> **Nota:** Os scores são cumulativos. Um release DUAL de um grupo bom terá score total maior que um legendado.

## 📦 Instalação do Recyclarr
[AQUI]](https://recyclarr.dev/wiki/installation/)

## 📝 Obtendo as API Keys

### Radarr
1. Acesse: **Configurações (Settings) → Geral (General) → Segurança (Security)**
2. Copie a **API Key**

### Sonarr
1. Acesse: **Configurações (Settings) → Geral (General) → Segurança (Security)**
2. Copie a **API Key**

## 📋 Paths Importantes

| Aplicação | Path Padrão | Docker Path |
|-----------|-------------|-------------|
| Recyclarr Config | `~/.config/recyclarr/recyclarr.yml` | `/config/recyclarr.yml` |
| Radarr | `http://localhost:7878` | `http://radarr:7878` |
| Sonarr | `http://localhost:8989` | `http://sonarr:8989` |

## 🔧 Combinando com TRaSH Guides

Você pode combinar estes Custom Formats com os oficiais do TRaSH:
> **💡 Dica:** Na pasta `recyclarr/` deste repositório existe um arquivo `recyclarr.yaml` com um exemplo completo de configuração que pode ser editado de acordo com suas necessidades.
```yaml
radarr:
  movies:
    custom_formats:
      # TRaSH Guides Oficiais (Áudio)
      - trash_ids:
          - 496f355514737f7d83bf7aa4d24f8169 # TrueHD Atmos
          - 2f22d89048b01681dde8afe203bf2e95 # DTS X
          - 3cafb66171b47f226146a0770576870f # TrueHD
        quality_profiles:
          - name: HD
            score: 500
      
      # TRaSH Guides Oficiais (HDR)
      - trash_ids:
          - e23edd2482476e595fb990b12e7c609c # DV HDR10
          - 58d6a88f13e2db7f5059c41047876f00 # DV
        quality_profiles:
          - name: HD
            score: 0
      
      # Custom Formats PT-BR (deste repositório)
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-dual
        quality_profiles:
          - name: HD
            score: 6000
      
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-dual
        quality_profiles:
          - name: HD
            score: 5500
      
      - base_url: https://raw.githubusercontent.com/SEU-USUARIO/trash-guides-ptbr/main/custom-formats
        trash_ids:
          - custom-web-tier-ptbr-not-group-radarr
        quality_profiles:
          - name: HD
            score: 5200
```

## ❓ Perguntas Frequentes

### Por que usar blocos separados para cada score?

No YAML, você não pode repetir chaves no mesmo bloco. Por isso, cada Custom Format com score diferente precisa estar em um bloco separado:

```yaml
# ❌ ERRADO - Não funciona
custom_formats:
  - base_url: https://...
    trash_ids:
      - custom-web-tier-ptbr-dual
    quality_profiles:
      - name: HD
        score: 6000
    trash_ids:  # ❌ Chave duplicada!
      - custom-web-tier-ptbr-not-dual

# ✅ CORRETO - Blocos separados
custom_formats:
  - base_url: https://...
    trash_ids:
      - custom-web-tier-ptbr-dual
    quality_profiles:
      - name: HD
        score: 6000

  - base_url: https://...
    trash_ids:
      - custom-web-tier-ptbr-not-dual
    quality_profiles:
      - name: HD
        score: 5500
```

### Como o Recyclarr busca os arquivos?

O Recyclarr faz download direto via HTTP:
1. Você define a `base_url` apontando para o GitHub (raw)
2. O Recyclarr concatena: `base_url` + `trash_id` + `.json`
3. Exemplo: `https://raw.githubusercontent.com/.../custom-formats/custom-web-tier-ptbr-dual.json`
4. A cada sync, ele baixa a versão mais recente

### Como atualizar os Custom Formats?

Basta fazer commit das alterações no GitHub. Na próxima execução do `recyclarr sync`, ele vai baixar a versão atualizada automaticamente.

## 📖 Links Úteis

- [Recyclarr Documentation](https://recyclarr.dev/)
- [TRaSH Guides](https://trash-guides.info/)
- [Radarr Wiki](https://wiki.servarr.com/radarr)
- [Sonarr Wiki](https://wiki.servarr.com/sonarr)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se livre para:
- Adicionar novos Custom Formats
- Melhorar os existentes
- Reportar bugs
- Sugerir melhorias

## 📄 Licença

MIT License - Sinta-se livre para usar e modificar.

---

**Última atualização:** Novembro 2025