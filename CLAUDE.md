# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Claude Code **skill** that lets users ask Claude to consult ChatGPT and Gemini before synthesizing an answer. The skill is triggered by phrases like "Consult the council: ..." or "Ask ChatGPT and Gemini what they think about ...".

## Key Commands

```bash
# Run the query script directly (requires .env with API keys)
python3 llm-council/scripts/query_llms.py "Your question here"

# Run all evals (requires API keys or local CLI tools)
python3 llm-council/scripts/run_evals.py

# Run a single eval case
python3 llm-council/scripts/run_evals.py --id trigger-01

# Run evals for one category
python3 llm-council/scripts/run_evals.py --category error-handling

# Benchmark: run each case N times, print mean/stdev/min/max
python3 llm-council/scripts/run_evals.py --benchmark 5

# Rebuild the packaged skill ZIP after any source change
python3 -c "
import zipfile, os
with zipfile.ZipFile('llm-council.skill', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('llm-council'):
        for f in files:
            fp = os.path.join(root, f)
            zf.write(fp, os.path.relpath(fp, 'llm-council'))
"
```

## Architecture

```
llm-council/          ← skill source (this is what gets packaged)
  SKILL.md            ← skill definition: trigger phrases, workflow, model options
  .env.template       ← copy to .env and add API keys
  scripts/
    query_llms.py     ← main script: queries ChatGPT + Gemini, outputs JSON
    run_evals.py      ← eval runner with benchmark support
  evals/
    eval_prompts.json ← 10 test cases (trigger, output-quality, error-handling)
    grading_criteria.md ← 6-dimension rubric (0–3 per dimension, 18 total)
  references/
    SETUP.md          ← API key setup instructions
llm-council.skill     ← ZIP of llm-council/ — the installable artifact
README.md             ← user-facing docs with install and usage examples
```

### Critical invariant: keep the ZIP in sync

`llm-council.skill` is a ZIP archive of the `llm-council/` directory. **Every time you edit any file inside `llm-council/`, you must rebuild the ZIP.** The rebuild command is above. If you forget, users install a stale skill.

### How `query_llms.py` works

CLI-first, API fallback:
1. Checks for `gemini` CLI and `codex` CLI in PATH
2. If CLI found → calls it (60s timeout)
3. If CLI not found or fails → calls API directly using keys from `.env`
4. Outputs a single JSON object: `{ prompt, chatgpt: { model, source, response }, gemini: { model, source, response } }`

`source` field values: `"gemini-cli"`, `"codex-cli"`, `"api (model-name)"`, or `"none"` (when both methods failed).

### Eval framework

`run_evals.py` exercises `query_llms.py` directly. Cases with `"should_trigger": false` are skipped (they test the skill-layer trigger logic, which requires a live Claude session to evaluate). The grading rubric in `grading_criteria.md` is for human/LLM-judge review of full skill output — `run_evals.py` only validates the script's JSON contract.

## Configuration

Copy `llm-council/.env.template` to `.env` in your working directory:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
OPENAI_MODEL=gpt-5-nano        # optional, this is the default
GEMINI_MODEL=gemini-3-flash-preview  # optional, this is the default
```

The script also reads `OPENAI_API_KEY` / `GEMINI_API_KEY` from the environment if `.env` is absent.

## Dependencies

Only stdlib + `requests`. No `requirements.txt` needed beyond:
```bash
pip install requests
```
