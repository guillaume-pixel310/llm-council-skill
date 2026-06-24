# Spec: Legal — Meeting Briefing

## Purpose

Generate a structured pre-meeting briefing for legal, business, or negotiation meetings: agenda, positions, leverage, talking points, red lines, and risks — so the user walks in prepared.

## Trigger

- `/legal:meeting-briefing`
- "Prepare a briefing for my meeting" / "Brief me on this meeting"
- "What should I know before my meeting with [party]?"
- "Help me prepare for a negotiation / contract discussion"
- "Prepare talking points for..."
- "I have a meeting with [company/party] about [topic] — help me prepare"

## Inputs

Gathered from the user (asked if missing):
1. Who the meeting is with
2. What it's about
3. The user's goal
4. Relevant background (relationship history, prior agreements, constraints)
5. Optionally, a document/contract/proposal to review first

## Outputs

A structured markdown briefing (see `legal/meeting-briefing/SKILL.md` for the exact template):
- Situation summary, key issues agenda table, objectives, their interests & leverage
- Talking points (opening statement, key points, anticipated pushback & responses)
- Red lines, open questions to raise, risks & contingencies, post-meeting next steps
- A "Quick Reference Card" for in-meeting use

Depth and focus adapt to meeting type: contract negotiation, dispute/conflict, vendor/partnership review, internal legal review, regulatory/compliance.

## Key files

- `legal/meeting-briefing/SKILL.md` — trigger phrases, information-gathering questions, output format, briefing-type variants, error handling
- `legal.skill` — packaged ZIP covering all `legal/` sub-skills, must stay in sync (CI-checked in `.github/workflows/evals.yml`)

## Constraints & non-goals

- Must ask the 4 gathering questions before generating a briefing if context is insufficient — does not fabricate meeting details
- Notes that legal-strategy recommendations are for preparation purposes only, not binding legal advice
- For complex meetings (many parties/issues), suggests focusing on the top 3 issues rather than attempting exhaustive coverage

## Open questions

- No automated eval suite exists for this skill yet (unlike `llm-council`) — quality is currently judged manually against the SKILL.md template.
