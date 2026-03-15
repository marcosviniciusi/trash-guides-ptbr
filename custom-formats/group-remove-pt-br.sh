#!/usr/bin/env bash
# Usage: ./group-remove-pt-br.sh GroupName1 GroupName2 GroupName3
# Removes release groups from the 6 Brazilian CF json files in current directory
#
# group-tier (negate=false, required=false):
#   custom-brazilian-group-tier-dual-audio.json
#   custom-brazilian-group-tier-subtitles.json
#   custom-brazilian-group-tier-dubbed.json
#
# deteccao (negate=true, required=true):
#   custom-brazilian-dual-language.json
#   custom-brazilian-subtitles.json
#   custom-brazilian-dubbed.json

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

FILES=$(find . -maxdepth 1 -type f \( \
  -name "custom-brazilian-group-tier-dual-audio.json" -o \
  -name "custom-brazilian-group-tier-subtitles.json" -o \
  -name "custom-brazilian-group-tier-dubbed.json" -o \
  -name "custom-brazilian-dual-language.json" -o \
  -name "custom-brazilian-subtitles.json" -o \
  -name "custom-brazilian-dubbed.json" \
\))

if [ -z "$FILES" ]; then
  echo "No matching files found in current directory."
  exit 1
fi

for file in $FILES; do
  echo "Processing: $file"

  python3 - "$file" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
groups_to_remove = set(sys.argv[2:])

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

removed = []
not_found = []

for group in groups_to_remove:
    found = any(s['name'] == group for s in data['specifications'])
    if found:
        removed.append(group)
    else:
        not_found.append(group)

data['specifications'] = [
    s for s in data['specifications']
    if s['name'] not in groups_to_remove
]

for g in removed:
    print(f"  REMOVED: {g}")
for g in not_found:
    print(f"  NOT FOUND: {g}")

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"  Done: {len(removed)} group(s) removed from {filepath}")
PYEOF

done

echo ""
echo "All files processed."