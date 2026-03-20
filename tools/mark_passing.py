"""Mark feature IDs as passing in feature_list.json. Usage: uv run python tools/mark_passing.py 1 2 3"""

from __future__ import annotations

import json
import sys
from pathlib import Path

feature_ids = {int(x) for x in sys.argv[1:]}
path = Path("feature_list.json")
data = json.loads(path.read_text(encoding="utf-8"))

for f in data:
    if f["id"] in feature_ids:
        f["passes"] = True
        print(f"Marked #{f['id']} as passing: {f['description'][:60]}...")

path.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("Done.")
