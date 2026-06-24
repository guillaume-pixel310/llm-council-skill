# .specify

Lightweight feature specs for this repo — one `spec.md` per feature, kept next to (not inside) the feature's source directory so specs survive even if source gets restructured.

This is not the full [GitHub Spec Kit](https://github.com/github/spec-kit) workflow (no `/specify`, `/plan`, `/tasks` slash commands or templates) — just plain markdown specs that describe what each feature does and why, for reference when extending or reviewing it.

## Convention

Each `spec.md` covers one feature and follows this shape:

- **Purpose** — what problem the feature solves, in one or two sentences
- **Trigger** — how it's invoked (slash command, phrase match, manual)
- **Inputs / Outputs** — what it consumes and produces
- **Key files** — where the implementation lives
- **Constraints & non-goals** — explicit boundaries, things it deliberately doesn't do
- **Open questions** — known gaps or unresolved decisions

## Current specs

| Feature | Spec | Source |
|---|---|---|
| LLM Council | [llm-council/spec.md](llm-council/spec.md) | `llm-council/` |
| Legal: Review Contract | [legal-review-contract/spec.md](legal-review-contract/spec.md) | `legal/review-contract/` |
| Legal: Meeting Briefing | [legal-meeting-briefing/spec.md](legal-meeting-briefing/spec.md) | `legal/meeting-briefing/` |
| Conseil des Agents | [conseil-agents/spec.md](conseil-agents/spec.md) | `conseil-agents/` |
| Astro Journal | [astro-journal/spec.md](astro-journal/spec.md) | `astro-journal/` |
| XIII SARL Pitch Deck | [xiii-sarl-pitch-deck/spec.md](xiii-sarl-pitch-deck/spec.md) | `xiii-sarl/` |
| XIII SARL Cashflow API | [xiii-sarl-cashflow-api/spec.md](xiii-sarl-cashflow-api/spec.md) | `xiii-sarl/cashflow-api/` |

When adding a new feature, add its `spec.md` here and list it in the table above.
