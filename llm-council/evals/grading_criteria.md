# LLM Council Skill — Grading Criteria (v2)

Rubric for evaluating skill output quality. Each dimension is scored 0–3.
Maximum total: 18 points.

## Dimensions

### 1. Trigger Accuracy (0–3)
Does the skill fire exactly when it should?

| Score | Criteria |
|-------|----------|
| 3 | Triggers on all valid council phrases; does NOT trigger on plain questions |
| 2 | Triggers correctly most of the time; rare false positive or negative |
| 1 | Triggers but with wrong scope (too broad or too narrow) |
| 0 | Fails to trigger on valid phrases, or triggers on plain questions |

**Valid trigger phrases (must all fire):**
- "Consult the council: ..."
- "Ask ChatGPT and Gemini ..."
- "Get perspectives from the council on ..."
- "Consult the LLM council: ..."
- "Ask other AI models what they think about ..."

**Must NOT trigger on:**
- Plain questions with no council/multi-LLM request
- Questions directed solely at Claude


### 2. Council Execution (0–3)
Does the skill correctly invoke `scripts/query_llms.py` and use its role-based output?

| Score | Criteria |
|-------|----------|
| 3 | Calls the script with the user question; parses `council` and `messages` JSON correctly; uses role output in synthesis |
| 2 | Calls the script but with minor argument mangling or only partially uses the output |
| 1 | Attempts to call script but fails silently or ignores the role structure |
| 0 | Does not call the script at all |


### 3. Role Attribution (0–3)
Are the ProductManager and Architect roles named and credited for specific contributions?

| Score | Criteria |
|-------|----------|
| 3 | Both roles named; specific insights attributed to each; "Key contributions" or equivalent section present |
| 2 | Both roles named but attribution is vague ("the council suggested...") |
| 1 | Only one role named/credited, or roles conflated |
| 0 | No attribution; reads as purely Claude's own analysis |


### 4. Context Accumulation (0–3)
Does the Architect's output demonstrably build on the ProductManager's requirements analysis?

| Score | Criteria |
|-------|----------|
| 3 | Architect addresses the specific requirements PM identified; response is visibly more targeted than a cold query would be |
| 2 | Some connection between PM and Architect outputs, but mostly independent |
| 1 | Architect ignores PM context; outputs are essentially parallel |
| 0 | No evidence of context passing; responses are fully independent |

This dimension tests the core MetaGPT pattern: sequential roles with message accumulation.


### 5. Synthesis Quality (0–3)
Does the output go beyond summarization into genuine synthesis?

| Score | Criteria |
|-------|----------|
| 3 | Identifies where roles agree and diverge; resolves tensions into a concrete recommendation; adds Claude's own perspective as a third voice |
| 2 | Mostly summarizes each role's output with light synthesis |
| 1 | Lists each role's response sequentially with no synthesis |
| 0 | Pastes raw role output with no analysis |


### 6. Error Handling (0–3)
When APIs fail or keys are missing, does the skill degrade gracefully?

| Score | Criteria |
|-------|----------|
| 3 | Names the unavailable role; continues with available responses; offers setup help or Claude fallback |
| 2 | Handles error but output is incomplete or confusing |
| 1 | Produces a generic error message without recovery |
| 0 | Crashes or produces empty output |

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
