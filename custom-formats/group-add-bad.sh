#!/usr/bin/env bash
# Usage: ./group-add-bad.sh GroupName1 GroupName2 GroupName3
# Adds release groups to custom-brazilian-group-tier-bad.json
# negate=false, required=false

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

FILE="custom-brazilian-group-tier-bad.json"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found in current directory."
  exit 1
fi

python3 - "$FILE" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
groups   = sys.argv[2:]

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
        "negate": False,
        "required": False,
        "fields": {
            "value": f"^({group})$"
        }
    }
    data['specifications'].append(entry)
    existing_names.add(group)
    added += 1
    print(f"  ADDED: {group}")

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"  Done: {added} group(s) added to {filepath}")
PYEOF
