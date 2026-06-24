## What & why

Short description of the change and the reason for it.

## Checklist

- [ ] If `llm-council/` or `legal/` source changed, `llm-council.skill` / `legal.skill` were rebuilt (the `.claude/rebuild-skill.sh` hook does this automatically when editing via Claude Code; otherwise rebuild manually — see `CLAUDE.md`)
- [ ] `python3 llm-council/scripts/run_evals.py` passes locally (if `llm-council/` changed)
- [ ] If a feature's behavior changed, its `.specify/<feature>/spec.md` was updated to match
- [ ] No API keys or secrets included in the diff

## Test plan

How you verified this works (commands run, eval output, manual testing).
