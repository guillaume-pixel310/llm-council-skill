# LLM Council Skill — Grading Criteria

Rubric for evaluating skill output quality. Each dimension is scored 0–3.

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


### 2. Script Execution (0–3)
Does the skill correctly invoke `scripts/query_llms.py`?

| Score | Criteria |
|-------|----------|
| 3 | Calls the script with the exact user question as argument; parses JSON correctly |
| 2 | Calls the script but with minor argument mangling |
| 1 | Attempts to call script but fails silently or ignores the output |
| 0 | Does not call the script at all |


### 3. Attribution (0–3)
Are ChatGPT and Gemini named and credited for specific insights?

| Score | Criteria |
|-------|----------|
| 3 | Both models named; specific insights attributed to each; "Key contributions" section present |
| 2 | Both models named but attribution is vague ("models suggested...") |
| 1 | Only one model named/credited |
| 0 | No attribution; reads as purely Claude's own analysis |


### 4. Synthesis Quality (0–3)
Does the output go beyond summarization into genuine synthesis?

| Score | Criteria |
|-------|----------|
| 3 | Identifies where models agree and disagree; resolves tensions into a concrete recommendation; adds Claude's own perspective |
| 2 | Mostly summarizes each model's view with light synthesis |
| 1 | Lists each model's response sequentially with no synthesis |
| 0 | Pastes raw model output with no analysis |


### 5. Actionability (0–3)
Is the response concretely useful — does it give the user something to act on?

| Score | Criteria |
|-------|----------|
| 3 | Includes concrete recommendations, specific tools/patterns, and next steps |
| 2 | Recommendations present but somewhat generic |
| 1 | Mostly informational with no clear path forward |
| 0 | No actionable guidance |


### 6. Error Handling (0–3)
When APIs fail or keys are missing, does the skill degrade gracefully?

| Score | Criteria |
|-------|----------|
| 3 | Names the unavailable model; continues with available responses; offers setup help or Claude fallback |
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
