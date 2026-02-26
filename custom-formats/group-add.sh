#!/usr/bin/env bash
# Usage: ./add_groups.sh GroupName1 GroupName2 GroupName3
# Adds release groups to all *-dual.json, *-gen.json, *-leg.json files in current directory

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 GroupName1 GroupName2 ..."
  exit 1
fi

# Find all target JSON files
FILES=$(find . -maxdepth 1 -type f \( -name "*-dual.json" -o -name "*-gen.json" -o -name "*-leg.json" \))

if [ -z "$FILES" ]; then
  echo "No *-dual.json, *-gen.json or *-leg.json files found in current directory."
  exit 1
fi

# Build the JSON block to insert (one entry per group)
build_entries() {
  local entries=""
  for group in "$@"; do
    entries+=$(printf '    ,\n    {\n      "name": "%s",\n      "implementation": "ReleaseGroupSpecification",\n      "negate": false,\n      "required": false,\n      "fields": {\n        "value": "^(%s)$"\n      }\n    }' "$group" "$group")
    entries+=$'\n'
  done
  echo "$entries"
}

ENTRIES=$(build_entries "$@")

for file in $FILES; do
  echo "Processing: $file"

  # Check if file ends with ] (closing the specifications array)
  # Insert before the last ]
  # Strategy: remove last line ("]"), append entries, then close

  # Use python for reliable JSON manipulation
  python3 - "$file" "$@" <<'PYEOF'
import sys
import json

filepath = sys.argv[1]
groups = sys.argv[2:]

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

done

echo ""
echo "All files processed."