# Spec: Legal — Review Contract

## Purpose

Give a structured, repeatable legal risk review of a contract or agreement: parties, obligations, liabilities, IP, termination, and a prioritized red/yellow/green flag list with negotiation recommendations.

## Trigger

- `/legal:review-contract`
- "Review this contract" / "Analyze this agreement" / "Check this contract for risks"
- "What are the red flags in this contract?"
- "Give me a legal review of..." / "Is this contract fair / reasonable?"

## Inputs

- Contract text (pasted), a file path, or a description of the contract. If none provided, the skill asks for it.

## Outputs

A structured markdown report (see `legal/review-contract/SKILL.md` for the exact template):
- Overview (parties, type, effective date, term, governing law)
- Risk Summary table
- Detailed Analysis: 🔴 Red Flags / 🟡 Cautions / 🟢 Standard clauses, each with quoted language and a recommendation
- Missing Clauses checklist
- Summary & prioritized next steps

## Key files

- `legal/review-contract/SKILL.md` — trigger phrases, analysis checklist (commercial terms, IP, liability, termination, confidentiality, dispute resolution, practical risks), output format, error handling
- `legal.skill` — packaged ZIP covering all `legal/` sub-skills, must stay in sync (CI-checked in `.github/workflows/evals.yml`)

## Constraints & non-goals

- Not a substitute for attorney review — the skill must note this is AI-assisted and recommend consulting a qualified attorney for binding decisions
- Does not attempt review without contract text — must ask rather than guess at clauses
- Flags translation uncertainty rather than refusing non-English contracts

## Open questions

- No automated eval suite exists for this skill yet (unlike `llm-council`) — quality is currently judged manually against the SKILL.md template.
