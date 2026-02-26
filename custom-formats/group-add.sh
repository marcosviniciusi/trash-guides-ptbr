#!/usr/bin/env bash
# Usage: ./add_groups.sh GroupName1 GroupName2 GroupName3
# Adds release groups to all *-dual.json, *-gen.json, *-leg.json files in current directory
# *-gen.json: negate=true, required=true
# *-dual.json, *-leg.json: negate=false, required=false

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

FILES=$(find . -maxdepth 1 -type f \( -name "*-dual.json" -o -name "*-gen.json" -o -name "*-leg.json" \))

if [ -z "$FILES" ]; then
  echo "No *-dual.json, *-gen.json or *-leg.json files found in current directory."
  exit 1
fi

for file in $FILES; do
  echo "Processing: $file"

  # Detect negate/required based on filename
  if [[ "$file" == *-gen.json ]]; then
    NEGATE="true"
    REQUIRED="true"
  else
    NEGATE="false"
    REQUIRED="false"
  fi

  python3 - "$file" "$NEGATE" "$REQUIRED" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
negate   = sys.argv[2] == "true"
required = sys.argv[3] == "true"
groups   = sys.argv[4:]

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_names = {s['name'] for s in data.get('specifications', [])}

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
            "value": f"^({group})$"
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