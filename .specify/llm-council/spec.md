# Spec: LLM Council

## Purpose

Let a user ask Claude to consult ChatGPT and Gemini before presenting an implementation plan, so the final recommendation synthesizes three models' perspectives instead of one.

## Trigger

Phrase match in `llm-council/SKILL.md` frontmatter — no slash command. Activates on prompts like:
- "Consult the council: ..."
- "Consult with ChatGPT and Gemini about..."
- "Ask ChatGPT and Gemini what they think about..."
- "Ask other AI models what they think about..."
- "Get perspectives from the council on..."
- "Consult the LLM council: ..."

Must NOT fire on prompts that don't match these patterns (verified by `no-trigger-*` eval cases).

## Inputs

- A user prompt/question (required)
- Optionally, a file path via `--file` (code, schema, config, document) whose content is appended to the prompt
- Optional `.env` in the working directory with `OPENAI_API_KEY`, `GEMINI_API_KEY`, `OPENAI_MODEL`, `GEMINI_MODEL`

## Outputs

- `scripts/query_llms.py` prints one JSON object to stdout: `{"prompt", "chatgpt": {"model", "source", "response"}, "gemini": {"model", "source", "response"}}`
- Claude then synthesizes a plan from Claude's own analysis + both responses, with inline attribution ("ChatGPT highlighted...", "Gemini suggested...") and a "Key contributions" summary

## Key files

- `llm-council/SKILL.md` — trigger phrases, workflow, output format
- `llm-council/scripts/query_llms.py` — CLI-first (codex/gemini), API-fallback (OpenAI/Gemini REST) query logic
- `llm-council/scripts/run_evals.py` — eval runner, JSON-contract validation, `--benchmark`
- `llm-council/evals/eval_prompts.json` — 13 cases across `trigger-recognition`, `output-quality`, `error-handling`
- `llm-council/evals/grading_criteria.md` — 6-dimension human/LLM-judge rubric
- `llm-council.skill` — packaged ZIP of `llm-council/`, must stay in sync (enforced by `.claude/rebuild-skill.sh` hook and `.github/workflows/evals.yml` CI check)

## Constraints & non-goals

- Only stdlib + `requests` — no other dependencies
- `query_llms.py` must never hard-fail when keys/CLIs are absent — it returns a descriptive error string and `source: "none"` so evals and CI can run with zero secrets configured
- Does not retry failed API calls or cache responses across invocations
- Does not let one model's failure block the other — partial results are synthesized

## Open questions

- None currently tracked. `run_evals.py` validates the JSON contract only, not response quality — quality review is manual via `grading_criteria.md`.
