# Spec: Conseil des Agents

## Purpose

A standalone, client-side multi-agent debate tool: 9 disciplinary personas argue a question in sequence, then an Arbitre (synthesizer) produces consensus, tensions, blind spots, and an actionable recommendation. Implements the operational side of the charter defined in `guillaume-os/17_CONSEIL_DES_13_AGENTS/constitution.md`.

## Trigger

Manual — the user opens `conseil-agents/index.html` in a browser and submits a question. No Claude Code skill trigger is involved; this runs entirely client-side.

## Inputs

- A question/decision submitted through the page's UI
- An Anthropic API key, entered once and stored in `localStorage` (`x-api-key` header), used for all subsequent calls directly from the browser

## Outputs

Sequential persona responses rendered in the UI, in order: Stratège, Financier, Juriste, Marketeur, Ops/Exécution, Psychologue, Innovateur, Contradicteur, Politicien, then the Arbitre's synthesis (consensus, unresolved tensions, collective blind spots, prioritized recommendation, main risk to watch).

## Key files

- `conseil-agents/index.html` — entire implementation: `AGENTS` array (id, icon, name, role, color, persona prompt per agent), debate loop, direct Anthropic API calls (model `claude-sonnet-4-6`)

## Constraints & non-goals

- Advisory only — per the constitution, the Council has no decision authority; it informs, the human decides
- The Contradicteur has a standing mandate to disagree — its persona prompt must not be softened to seek consensus
- Agent count is currently 10 (9 disciplines + Arbitre); the constitution's "13 Agents" name anticipates 3 more undefined seats — adding them requires updating the constitution's Article 2 table first, then this file
- No server component, no persistence of debate history beyond what the constitution's README tracks manually in its consultation-history table
- API key handling is client-side only (`localStorage`) — there is no backend proxy or key rotation

## Open questions

- 3 of the named "13 Agents" seats remain unfilled (tracked as the open task in `guillaume-os/17_CONSEIL_DES_13_AGENTS/constitution.md`, Article 2)
- No automated tests cover this file — it has no eval suite, unlike `llm-council`
