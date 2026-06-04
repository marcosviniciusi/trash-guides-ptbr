#!/usr/bin/env bash
# Usage: ./compare_groups.sh
# Compares release groups in Brazilian CF files against custom-us-group-tier-premium.json
# Reports any group names that appear in both

set -euo pipefail

US_FILE="custom-us-group-tier-premium.json"

BR_FILES=(
  "custom-brazilian-group-tier-dual-audio.json"
  "custom-brazilian-group-tier-subtitles.json"
  "custom-brazilian-group-tier-dubbed.json"
  "custom-brazilian-subtitles.json"
  "custom-brazilian-dubbed.json"
)

if [ ! -f "$US_FILE" ]; then
  echo "Error: $US_FILE not found in current directory."
  exit 1
fi

found_any=false

for br_file in "${BR_FILES[@]}"; do
  if [ ! -f "$br_file" ]; then
    echo "SKIP (not found): $br_file"
    continue
  fi

  python3 - "$US_FILE" "$br_file" <<'PYEOF'
import sys
import json

us_file = sys.argv[1]
br_file = sys.argv[2]

with open(us_file, 'r', encoding='utf-8') as f:
    us_data = json.load(f)

with open(br_file, 'r', encoding='utf-8') as f:
    br_data = json.load(f)

us_names = {s['name'] for s in us_data.get('specifications', []) if s.get('implementation') == 'ReleaseGroupSpecification'}
br_names = {s['name'] for s in br_data.get('specifications', []) if s.get('implementation') == 'ReleaseGroupSpecification'}

overlap = sorted(us_names & br_names)

if overlap:
    print(f"\n  [{br_file}] — {len(overlap)} duplicate(s) found in {us_file}:")
    for name in overlap:
        print(f"    - {name}")
else:
    print(f"\n  [{br_file}] — no duplicates with {us_file}")
PYEOF

done

echo ""
echo "Done."