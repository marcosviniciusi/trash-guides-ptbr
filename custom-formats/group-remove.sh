#!/usr/bin/env bash
# Usage: ./remove_groups.sh GroupName1 GroupName2 GroupName3
# Removes release groups from all *-dual.json, *-gen.json, *-leg.json files in current directory

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

  python3 - "$file" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
groups_to_remove = set(sys.argv[2:])

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data.get('specifications', []))
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