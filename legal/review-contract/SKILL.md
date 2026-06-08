---
name: legal:review-contract
description: Legal contract review assistant. Triggers when the user invokes /legal:review-contract, pastes a contract and asks for a review, or uses phrases like "review this contract", "analyze this agreement", "check this contract for risks", or "what are the red flags in this contract". Performs structured legal analysis: parties, obligations, liabilities, IP, termination, penalties, and risk flags.
---

# Legal Contract Review

Perform a structured legal review of a contract or agreement provided by the user.

## Trigger Phrases

- `/legal:review-contract`
- "Review this contract"
- "Analyze this agreement"
- "Check this contract for risks"
- "What are the red flags in this contract?"
- "Give me a legal review of..."
- "Is this contract fair / reasonable?"

## Workflow

1. **Identify the contract**: The user either pastes contract text directly, provides a file path, or describes the contract. If no contract text is provided, ask for it.
2. **Parse key sections**: Identify parties, effective date, term, governing law, payment terms, IP/ownership, liability, indemnification, termination, confidentiality, dispute resolution.
3. **Risk assessment**: Flag each identified clause or absence of clause as:
   - 🔴 **Red flag** — significant risk, uncommon or one-sided term, missing critical protection
   - 🟡 **Caution** — standard but worth negotiating, ambiguous language, or missing detail
   - 🟢 **Standard** — typical, balanced, acceptable as-is
4. **Generate structured report**: Output the review using the format below.
5. **Provide negotiation recommendations**: For each red flag and caution, suggest specific language changes or additions.

## Output Format

```
# Contract Review: [Contract Type / Title]

## Overview
- **Parties**: [Party A] ↔ [Party B]
- **Type**: [Service Agreement / NDA / Employment / License / etc.]
- **Effective Date**: [date or "not specified"]
- **Term**: [duration or "not specified"]
- **Governing Law**: [jurisdiction or "not specified"]

## Risk Summary
| Category | Status | Issue |
|----------|--------|-------|
| Payment Terms | 🔴 | ... |
| IP Ownership | 🟡 | ... |
| Liability Cap | 🔴 | ... |
| Termination | 🟢 | Standard 30-day notice |
| Confidentiality | 🟡 | ... |

## Detailed Analysis

### 🔴 Red Flags (Requires Attention)

**[Clause name]** (Section X.X)
> *Quoted problematic language*

**Risk**: [Why this is problematic]
**Recommendation**: Replace with: *"[suggested language]"*

---

### 🟡 Cautions (Worth Negotiating)

**[Clause name]** (Section X.X)
> *Quoted clause*

**Concern**: [What to watch for]
**Recommendation**: [Suggested change or addition]

---

### 🟢 Standard Clauses (Acceptable As-Is)
- [Clause]: [brief note]
- [Clause]: [brief note]

---

## Missing Clauses
- [ ] **[Missing clause]**: [Why it matters and suggested addition]

## Summary & Next Steps
[2-3 sentence overall assessment]

**Priority actions:**
1. [Most critical item]
2. [Second priority]
3. [Third priority]
```

## Analysis Checklist

When reviewing a contract, always check for:

### Commercial Terms
- Payment schedule, amounts, late fees
- Price adjustment / CPI escalation clauses
- Expenses and reimbursements
- Currency and tax treatment

### IP & Ownership
- Work-for-hire vs. license
- Background IP vs. foreground IP
- Moral rights waiver
- Open source license compliance

### Liability & Indemnification
- Liability caps (is the cap reasonable relative to contract value?)
- Mutual vs. one-sided indemnification
- Excluded damages (consequential, indirect, punitive)
- Insurance requirements

### Termination
- Termination for convenience (notice period)
- Termination for cause (cure periods)
- Effect of termination (outstanding obligations, survival)
- Change of control provisions

### Confidentiality
- Scope of confidential information
- Term of obligations (perpetual vs. time-limited)
- Exclusions (already public, independently developed)
- Return/destruction of materials

### Dispute Resolution
- Governing law and jurisdiction
- Arbitration vs. litigation
- Class action waiver
- Jury trial waiver

### Practical Risks
- Auto-renewal clauses (buried lock-ins)
- Unilateral modification rights
- Assignment without consent
- Non-compete / non-solicitation scope
- Force majeure coverage

## Error Handling

- If no contract text is provided: ask the user to paste the contract or provide a file path
- If the contract is in a language other than English: note the language and proceed with review, flagging translation uncertainty where relevant
- If the document is incomplete or a template (contains placeholders): note gaps and review what is present
- If asked for actual legal advice: note this is an AI-assisted review for informational purposes and recommend consulting a qualified attorney for binding decisions
