# Legal Skill — Grading Criteria

Rubric for evaluating `legal:review-contract` and `legal:meeting-briefing` output quality. Each dimension is scored 0–3 (18 total per skill).

---

## legal:review-contract

### 1. Trigger Accuracy (0–3)
Does the skill fire on contract review requests and not on general legal questions?

| Score | Criteria |
|-------|----------|
| 3 | Triggers on all valid phrases and explicit command; does NOT trigger on general questions |
| 2 | Triggers correctly most of the time; rare false positive or negative |
| 1 | Too broad (triggers on any legal question) or too narrow (only fires on slash command) |
| 0 | Fails to trigger on valid contract review requests, or triggers on unrelated queries |

**Must trigger on:**
- `/legal:review-contract`
- "Review this contract"
- "What are the red flags in this agreement?"
- "Check this contract for risks"
- "Analyze this [NDA / service agreement / employment contract]"

**Must NOT trigger on:**
- "What is a contract?"
- "Tell me about contract law"
- "Should I sign this?" (without a contract present)


### 2. Structure & Completeness (0–3)
Does the output use the defined report format?

| Score | Criteria |
|-------|----------|
| 3 | Includes Overview, Risk Summary table, Detailed Analysis with 🔴/🟡/🟢 flags, Missing Clauses, and Summary |
| 2 | Most sections present but one is missing or poorly formed |
| 1 | Partial structure; reads more like a prose summary than a structured review |
| 0 | No structure; generic narrative with no flags or sections |


### 3. Risk Identification (0–3)
Are genuine risks correctly identified and flagged?

| Score | Criteria |
|-------|----------|
| 3 | Identifies all significant risks in the contract; no material risks missed; flags are correctly calibrated (red vs. yellow) |
| 2 | Identifies most risks but misses 1-2 significant issues or miscalibrates some flags |
| 1 | Identifies obvious surface-level issues only; misses structural or subtle risks |
| 0 | Misses major risks or flags benign clauses as high risk |


### 4. Actionability of Recommendations (0–3)
Are recommendations specific and usable?

| Score | Criteria |
|-------|----------|
| 3 | Each red flag includes specific replacement language; each caution includes a concrete suggestion; priority actions are ranked |
| 2 | Recommendations present but vague ("negotiate this clause") without specific language |
| 1 | General advice ("seek legal counsel") without clause-specific guidance |
| 0 | No recommendations; review only states problems without suggesting solutions |


### 5. Missing Clause Detection (0–3)
Does the skill identify clauses that should be present but aren't?

| Score | Criteria |
|-------|----------|
| 3 | Identifies all material missing clauses for the contract type; explains why each matters |
| 2 | Identifies most missing clauses; misses 1-2 common protections |
| 1 | Notes some gaps but without specificity about what's needed |
| 0 | Does not check for missing clauses at all |


### 6. Error Handling (0–3)
When no contract is provided or the document is incomplete, does the skill handle it well?

| Score | Criteria |
|-------|----------|
| 3 | Asks for contract text clearly; does not fabricate a review; explains what to provide |
| 2 | Asks for input but the request is unclear or incomplete |
| 1 | Produces a generic review or refuses without helpful guidance |
| 0 | Fabricates a contract review with no input, or crashes silently |

---

## legal:meeting-briefing

### 1. Trigger Accuracy (0–3)
Does the skill fire on meeting preparation requests?

| Score | Criteria |
|-------|----------|
| 3 | Triggers on all valid preparation phrases; does NOT trigger on casual meeting questions |
| 2 | Triggers correctly most of the time |
| 1 | Too broad or too narrow |
| 0 | Misses valid triggers or fires on unrelated queries |


### 2. Context Gathering (0–3)
Does the skill gather enough information before generating the briefing?

| Score | Criteria |
|-------|----------|
| 3 | Asks all 4 gathering questions when context is missing; proceeds directly when context is clear |
| 2 | Asks some questions but misses key context (e.g., doesn't ask about goals) |
| 1 | Generates a briefing without sufficient context; result is generic |
| 0 | Ignores missing context entirely; produces an irrelevant briefing |


### 3. Issue Identification (0–3)
Are the key issues for the meeting correctly identified?

| Score | Criteria |
|-------|----------|
| 3 | Identifies all major issues; accurately infers each party's likely position; notes conflicts correctly |
| 2 | Identifies main issues but misses secondary ones or misreads one party's position |
| 1 | Surface-level issue identification; reads as generic meeting advice |
| 0 | Issues are wrong, irrelevant, or not identified at all |


### 4. Talking Points Quality (0–3)
Are the talking points specific, strategic, and usable?

| Score | Criteria |
|-------|----------|
| 3 | Talking points are specific to the situation; includes rationale; objection responses are realistic and sharp |
| 2 | Talking points are relevant but somewhat generic; objection responses present but weak |
| 1 | Talking points are too general to be useful in the specific meeting |
| 0 | No meaningful talking points; briefing is a generic meeting template |


### 5. Strategic Framing (0–3)
Does the briefing help the user understand their leverage, risks, and walk-away position?

| Score | Criteria |
|-------|----------|
| 3 | Clearly identifies leverage, BATNA/walk-away, and risks for both sides; red lines are explicit |
| 2 | Most strategic elements present but one is missing or underdeveloped |
| 1 | Little strategic framing; reads like a factual summary, not a negotiation tool |
| 0 | No strategic content; purely descriptive |


### 6. Error Handling (0–3)
When insufficient context is given, does the skill handle it gracefully?

| Score | Criteria |
|-------|----------|
| 3 | Asks the 4 gathering questions clearly; does not invent meeting details; explains what it needs |
| 2 | Asks for some context but misses key questions |
| 1 | Generates a placeholder briefing that's too generic to be useful |
| 0 | Fabricates meeting details or produces no output |

---

## Scoring

| Total Score | Grade | Interpretation |
|-------------|-------|----------------|
| 16–18 | A | Production-ready |
| 13–15 | B | Minor improvements needed |
| 10–12 | C | Significant gaps |
| 7–9  | D | Needs rework |
| 0–6  | F | Failing |

**Minimum passing score per dimension: 2**
A skill that scores 0 or 1 on any single dimension fails regardless of total score.
