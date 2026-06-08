#!/bin/bash
# PostToolUse hook: rebuild llm-council.skill when any source file changes.
# Reads tool input JSON from stdin; exits 0 always (non-blocking).

input=$(cat)
file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)

# Only rebuild when the edited file is inside llm-council/
if [[ "$file_path" == *"llm-council/"* ]]; then
    root=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
    python3 -c "
import zipfile, os
root = '$root'
os.chdir(root)
with zipfile.ZipFile('llm-council.skill', 'w', zipfile.ZIP_DEFLATED) as zf:
    for r, _, files in os.walk('llm-council'):
        for f in files:
            fp = os.path.join(r, f)
            zf.write(fp, os.path.relpath(fp, 'llm-council'))
print('[hook] Rebuilt llm-council.skill')
"
fi

exit 0
