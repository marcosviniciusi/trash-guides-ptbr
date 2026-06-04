#!/usr/bin/env bash
# Usage: ./group-add-pt-br.sh GroupName1 GroupName2 GroupName3
# Adds release groups to the 5 Brazilian CF json files in current directory
#
# negate=false, required=false (group-tier - match positivo):
#   custom-brazilian-group-tier-dual-audio.json
#   custom-brazilian-group-tier-subtitles.json
#   custom-brazilian-group-tier-dubbed.json
#
# negate=true, required=true (deteccao - exclui grupo da regex geral):
#   custom-brazilian-subtitles.json
#   custom-brazilian-dubbed.json
#
# NOTE: custom-brazilian-dual-language.json uses only LanguageSpecification
# (PT + Original Language) and does NOT take ReleaseGroupSpecification entries.

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

FILES=$(find . -maxdepth 1 -type f \( \
  -name "custom-brazilian-group-tier-dual-audio.json" -o \
  -name "custom-brazilian-group-tier-subtitles.json" -o \
  -name "custom-brazilian-group-tier-dubbed.json" -o \
  -name "custom-brazilian-subtitles.json" -o \
  -name "custom-brazilian-dubbed.json" \
\))

if [ -z "$FILES" ]; then
  echo "No matching files found in current directory."
  exit 1
fi

for file in $FILES; do
  echo "Processing: $file"

  basename=$(basename "$file")

  case "$basename" in
    "custom-brazilian-group-tier-dual-audio.json"|"custom-brazilian-group-tier-subtitles.json"|"custom-brazilian-group-tier-dubbed.json")
      NEGATE="false"
      REQUIRED="false"
      ;;
    "custom-brazilian-subtitles.json"|"custom-brazilian-dubbed.json")
      NEGATE="true"
      REQUIRED="true"
      ;;
  esac

  python3 - "$file" "$NEGATE" "$REQUIRED" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
negate   = sys.argv[2] == "true"
required = sys.argv[3] == "true"
groups   = sys.argv[4:]

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

all_names = [s['name'] for s in data.get('specifications', [])]
seen = set()
dupes_in_file = []
for n in all_names:
    if n in seen:
        dupes_in_file.append(n)
    seen.add(n)

if dupes_in_file:
    print(f"  WARNING: existing duplicates in file: {dupes_in_file}")

existing_names = set(all_names)
added = 0
for group in groups:
    if group in existing_names:
        print(f"  SKIP (already exists): {group}")
        continue
    entry = {
        "name": group,
        "implementation": "ReleaseGroupSpecification",
        "negate": negate,
        "required": required,
        "fields": {
            "value": f"(?:^|-){group}$"
        }
    }
    data['specifications'].append(entry)
    existing_names.add(group)
    added += 1
    print(f"  ADDED: {group} (negate={str(negate).lower()}, required={str(required).lower()})")

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"  Done: {added} group(s) added to {filepath}")
PYEOF

done

echo ""
echo "All files processed."