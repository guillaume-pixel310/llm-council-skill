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

# Run evals with verbose output
python3 llm-council/scripts/run_evals.py --verbose

# Benchmark: run each case N times, print mean/stdev/min/max
python3 llm-council/scripts/run_evals.py --benchmark 5

# Manually rebuild the packaged skill ZIP after any source change
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
llm-council/              ← skill source (this is what gets packaged)
  SKILL.md                ← skill definition: trigger phrases, workflow, model options
  .env.template           ← copy to .env and add API keys
  scripts/
    query_llms.py         ← main script: queries ChatGPT + Gemini, outputs JSON
    run_evals.py          ← eval runner with benchmark support
  evals/
    eval_prompts.json     ← 10 test cases (trigger, output-quality, error-handling)
    grading_criteria.md   ← 6-dimension rubric (0–3 per dimension, 18 total)
  references/
    SETUP.md              ← API key setup instructions
llm-council.skill         ← ZIP of llm-council/ — the installable artifact
.claude/
  settings.json           ← PostToolUse hook that auto-rebuilds the skill ZIP
  rebuild-skill.sh        ← hook script: rebuilds ZIP when llm-council/ files change
README.md                 ← user-facing docs with install and usage examples
```

### Critical invariant: keep the ZIP in sync

`llm-council.skill` is a ZIP archive of the `llm-council/` directory. A `PostToolUse` hook in `.claude/settings.json` fires `.claude/rebuild-skill.sh` automatically whenever you edit a file inside `llm-council/` via Claude Code's Edit or Write tools. The script reads the edited file path from stdin (tool input JSON), checks it's inside `llm-council/`, then rebuilds the ZIP. If you edit files outside Claude Code (e.g., directly in an editor), run the rebuild command above manually.

### How `query_llms.py` works

CLI-first, API fallback strategy:

1. Loads `.env` from the **current working directory** (not from `llm-council/`)
2. Also reads `OPENAI_API_KEY` / `GEMINI_API_KEY` / `OPENAI_MODEL` / `GEMINI_MODEL` from the process environment if `.env` is absent or incomplete
3. Checks for `gemini` and `codex` CLIs in PATH using `shutil.which`
4. **For ChatGPT**: tries `codex -p <prompt>` first (60s timeout); on failure falls back to OpenAI REST API (30s timeout)
5. **For Gemini**: tries `gemini -p <prompt>` first (60s timeout); on failure falls back to Gemini REST API (30s timeout)
6. Both API calls use `temperature=0.7` and `max_tokens=2000`
7. Outputs a single JSON object to stdout:
   ```json
   {
     "prompt": "...",
     "chatgpt": { "model": "gpt-5-nano", "source": "codex-cli", "response": "..." },
     "gemini":  { "model": "gemini-3-flash-preview", "source": "gemini-cli", "response": "..." }
   }
   ```

`source` field values: `"codex-cli"`, `"gemini-cli"`, `"api (model-name)"`, or `"none"` (when both CLI and API failed).

### Skill trigger phrases

The skill activates on these user patterns (defined in `SKILL.md` frontmatter):

- "Consult the council: ..."
- "Consult with ChatGPT and Gemini about..."
- "Ask ChatGPT and Gemini what they think about..."
- "Ask other AI models what they think about..."
- "Get perspectives from the council on..."
- "Consult the LLM council: ..."

Non-matching prompts must **not** trigger the skill — tested by `no-trigger-*` eval cases.

### Skill workflow

1. Execute `scripts/query_llms.py` with the user's prompt
2. Parse the JSON response from both models
3. Synthesize an implementation plan incorporating Claude's own analysis + ChatGPT + Gemini insights
4. Present the plan with inline attribution ("ChatGPT highlighted...", "Gemini suggested...")
5. End with a "Key contributions" summary crediting each model

### Eval framework

`run_evals.py` exercises `query_llms.py` directly. It:

- Loads cases from `evals/eval_prompts.json` (10 cases across 3 categories: `trigger-recognition`, `output-quality`, `error-handling`)
- Skips cases with `"should_trigger": false` — those test the skill-layer trigger logic, which requires a live Claude session
- For each runnable case, validates the JSON contract: required keys (`prompt`, `chatgpt`, `gemini`), non-empty responses, and source tracking
- `--benchmark N` runs each case N times and reports mean/stdev/min/max latency

The grading rubric in `grading_criteria.md` is for human/LLM-judge review of full skill output — `run_evals.py` only validates the script's JSON contract, not response quality.

### Grading rubric (for human/LLM review)

Six dimensions, 0–3 each (18 total):

1. **Trigger Accuracy** — skill fires exactly when and only when it should
2. **Script Execution** — `query_llms.py` invoked correctly with the right prompt
3. **Attribution** — ChatGPT and Gemini are named and credited for specific insights
4. **Synthesis Quality** — goes beyond summarization into genuine synthesis
5. **Actionability** — concrete recommendations with specific tools and next steps
6. **Error Handling** — graceful degradation when one or both APIs fail

Scoring: 16–18 = A (production-ready), 13–15 = B, 10–12 = C, 7–9 = D, 0–6 = F. Any dimension scoring 0–1 is a failing condition regardless of total.

## Configuration

Copy `llm-council/.env.template` to `.env` in your **working directory** (where you run scripts from):

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
OPENAI_MODEL=gpt-5-nano           # optional, this is the default
GEMINI_MODEL=gemini-3-flash-preview  # optional, this is the default
```

### Model options

**OpenAI (ordered by capability/cost):**
| Model | Notes | Cost |
|---|---|---|
| `gpt-5-nano` | Default. Fastest, most cost-efficient | $0.05/1M in, $0.40/1M out |
| `gpt-5-mini` | Faster for well-defined tasks | $0.25/1M in, $2.00/1M out |
| `gpt-5.2` | Best for coding and agentic tasks | $1.75/1M in, $14.00/1M out |
| `gpt-5.2-pro` | Highest capability | $21.00/1M in, $168.00/1M out |

**Gemini (ordered by capability):**
| Model | Notes |
|---|---|
| `gemini-2.5-flash-lite` | Ultra-fast, optimized for throughput |
| `gemini-2.5-flash` | Best price-performance |
| `gemini-3-flash-preview` | Default. Balanced speed and frontier intelligence |
| `gemini-3-pro-preview` | Most intelligent, best for complex reasoning |

## Dependencies

Only stdlib + `requests`. No `requirements.txt` needed beyond:

```bash
pip install requests
```
