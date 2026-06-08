---
name: legal:meeting-briefing
description: Legal meeting briefing generator. Triggers when the user invokes /legal:meeting-briefing, or uses phrases like "prepare a briefing for my meeting", "brief me on this meeting", "what should I know before this meeting", "prepare talking points for...", or "help me prepare for a meeting with [party]". Generates a structured pre-meeting briefing covering agenda, key issues, positions, risks, and recommended talking points.
---

# Legal Meeting Briefing

Generate a structured briefing document to prepare for an upcoming meeting involving legal, business, or negotiation matters.

## Trigger Phrases

- `/legal:meeting-briefing`
- "Prepare a briefing for my meeting"
- "Brief me on this meeting"
- "What should I know before my meeting with [party]?"
- "Help me prepare for a negotiation / contract discussion"
- "Prepare talking points for..."
- "I have a meeting with [company/party] about [topic] — help me prepare"

## Workflow

1. **Gather meeting context**: Ask for (or extract from user's message):
   - Meeting purpose (negotiation, review, kick-off, dispute, etc.)
   - Parties involved (who's attending, their roles/interests)
   - Subject matter (contract, project, dispute, partnership, etc.)
   - Prior history (existing relationship, previous agreements, open issues)
   - Your goals for the meeting
   - Any documents or context to review

2. **Analyze the situation**: Identify:
   - Key issues likely to be raised
   - Areas of alignment vs. potential conflict
   - Your leverage points and the other party's leverage
   - Risks if the meeting goes poorly
   - Desired outcomes (best case, acceptable, walk-away)

3. **Generate briefing document**: Use the format below.

## Information Gathering

If the user hasn't provided enough context, ask:

1. **Who is the meeting with?** (Company, individual, role/title)
2. **What is the meeting about?** (Topic, contract, dispute, negotiation)
3. **What is your goal?** (What do you want to achieve?)
4. **Any background I should know?** (Existing relationship, previous issues, key constraints)

If the user provides a contract, proposal, or document — read it first before generating the briefing.

## Output Format

```
# Meeting Briefing: [Meeting Topic]
**Date**: [date if known]
**Meeting With**: [Party / Person / Company]
**Your Role**: [Your position / company]
**Purpose**: [One-line purpose statement]

---

## Situation Summary
[2-3 sentences: what's happening, why this meeting matters, what's at stake]

---

## Key Issues Agenda

| # | Issue | Your Position | Their Likely Position | Priority |
|---|-------|--------------|----------------------|----------|
| 1 | [Issue] | [Your stance] | [Their likely stance] | High |
| 2 | ... | ... | ... | Medium |

---

## Your Objectives

**Primary goal**: [Non-negotiable outcome you need]
**Secondary goals**: [Nice-to-haves, fallback positions]
**Walk-away condition**: [When you would end negotiations / not proceed]

---

## Their Interests & Leverage
- **What they want**: [Their likely objectives]
- **Their constraints**: [Deadlines, budget, dependencies]
- **Their leverage**: [What gives them power in this negotiation]
- **Your leverage**: [What gives you power]

---

## Talking Points

### Opening Statement
[How to open the meeting — set tone, establish your position]

### Key Points to Make
1. [Point 1 — with supporting rationale]
2. [Point 2 — with supporting rationale]
3. [Point 3 — with supporting rationale]

### Anticipated Pushback & Responses
| Their Objection | Your Response |
|-----------------|---------------|
| "[Likely objection]" | "[Your counter]" |
| "[Likely objection]" | "[Your counter]" |

---

## Red Lines & Non-Negotiables
- [Item you will not concede on, and why]
- [Item you will not concede on, and why]

---

## Open Questions to Raise
- [ ] [Question you need answered in this meeting]
- [ ] [Clarification needed]
- [ ] [Commitment to request]

---

## Risks & Contingencies
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [How to handle] |

---

## Recommended Next Steps (Post-Meeting)
1. [Follow-up action 1]
2. [Follow-up action 2]
3. [Send/request documents]

---

## Quick Reference Card
*(For use during the meeting)*

**Must achieve**: [One thing]
**Can concede**: [One thing]
**Avoid**: [One thing]
**Key number / date / term to remember**: [Critical detail]
```

## Briefing Types

Adapt the depth and focus based on meeting type:

### Contract Negotiation
- Focus on key commercial terms, red lines, BATNA
- Include clause-by-clause position table if a draft exists
- Note any regulatory or compliance constraints

### Dispute / Conflict Meeting
- Include timeline of events leading to dispute
- Identify facts in dispute vs. facts agreed
- Note potential legal exposure on both sides
- Preferred resolution (settlement, correction, etc.)

### Vendor / Partnership Review
- Relationship history and performance metrics
- Key concerns to address
- Renewal / expansion / exit considerations

### Internal Legal Review
- Decision being sought from stakeholders
- Legal risks and mitigation options
- Recommendation with rationale

### Regulatory / Compliance Meeting
- Relevant regulations and current compliance status
- Open items and remediation timeline
- Key questions for the regulator

## Error Handling

- If insufficient context is provided: ask the 4 gathering questions before generating the briefing
- If a document is referenced but not provided: ask the user to paste or share it
- If the meeting is complex (many parties, many issues): suggest breaking into sub-sections or focusing on the top 3 issues
- If asked for legal strategy advice: note this briefing is for preparation purposes and recommend consulting a qualified attorney for matters with significant legal exposure
