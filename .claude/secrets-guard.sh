#!/bin/bash
# PreToolUse hook: warn before reading files that may contain secrets.
# Exits 2 (block) if the target is a .env file with real credentials.
# Exits 0 (allow) otherwise.

input=$(cat)
file_path=$(echo "$input" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)

# Block reads of .env (the real secrets file, not the template)
if [[ "$file_path" == *"/.env" ]] || [[ "$file_path" == ".env" ]]; then
    echo "[secrets-guard] Blocked: .env contains live API keys and should not be read into LLM context. Use .env.template to review the format." >&2
    exit 2
fi

exit 0
