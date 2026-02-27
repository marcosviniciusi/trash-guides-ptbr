#!/usr/bin/env bash
# Usage: ./remove_groups_premium.sh GroupName1 GroupName2 GroupName3
# Removes release groups from custom-us-group-tier-premium.json

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

FILE="custom-us-group-tier-premium.json"

if [ ! -f "$FILE" ]; then
  echo "Error: $FILE not found in current directory."
  exit 1
fi

python3 - "$FILE" "$@" <<'PYEOF'
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