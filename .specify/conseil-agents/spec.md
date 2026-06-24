# Spec: Conseil des Agents

## Purpose

A standalone, client-side multi-agent debate tool: disciplinary personas argue a question in sequence, then an Arbitre (synthesizer) produces consensus, tensions, blind spots, and an actionable recommendation. Implements the operational side of the charter defined in `guillaume-os/17_CONSEIL_DES_13_AGENTS/constitution.md`. All 13 seats defined in the constitution are now implemented: 12 disciplines + the Arbitre.

## Trigger

Manual — the user opens `conseil-agents/index.html` in a browser and submits a question. No Claude Code skill trigger is involved; this runs entirely client-side.

## Inputs

- A question/decision submitted through the page's UI
- An Anthropic API key, entered once and stored in `localStorage` (`x-api-key` header), used for all subsequent calls directly from the browser

## Outputs

Sequential persona responses rendered in the UI, in order: Stratège, Financier, Juriste, Marketeur, Ops/Exécution, Psychologue, Innovateur, Contradicteur, Politicien, Fiscaliste International, Conseiller Familial, Stratège de Transmission, then the Arbitre's synthesis (consensus, unresolved tensions, collective blind spots, prioritized recommendation, main risk to watch).

## Key files

- `conseil-agents/index.html` — entire implementation: `AGENTS` array (id, icon, name, role, color, persona prompt per agent), debate loop, direct Anthropic API calls (model `claude-sonnet-4-6`)

## Constraints & non-goals

- Advisory only — per the constitution, the Council has no decision authority; it informs, the human decides
- The Contradicteur has a standing mandate to disagree — its persona prompt must not be softened to seek consensus
- Implemented agent count is now 13 (12 disciplines + Arbitre), matching all seats defined in the constitution (Article 2); any future composition change must be reflected in the constitution first, before being implemented here, per Article 8
- No server component, no persistence of debate history beyond what the constitution's README tracks manually in its consultation-history table
- API key handling is client-side only (`localStorage`) — there is no backend proxy or key rotation

## Open questions

- No automated tests cover this file — it has no eval suite, unlike `llm-council`
