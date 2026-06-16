---
name: llm-council
description: Multi-LLM collaborative brainstorming and planning. Use when user explicitly requests consultation with multiple AI models (ChatGPT, Gemini, other LLMs) before presenting an implementation plan, or asks to "consult the council", "ask the council", "ask ChatGPT and Gemini", "ask other models", or "get perspectives from other AIs". Queries external LLM APIs, synthesizes their perspectives, and presents an adapted implementation plan.
---

# LLM Council

Consult multiple AI models (ChatGPT and Gemini) for their perspectives before presenting implementation plans to users.

## Workflow

When user requests consultation with other AI models, use phrases like:
- "Consult the council: [your question]"
- "Consult with ChatGPT and Gemini about..."
- "Ask ChatGPT and Gemini what they think about..."
- "Ask other AI models what they think about..."
- "Get perspectives from the council on..."
- "Consult the LLM council: [your question]"

**Process:**

1. **Query external LLMs**: Run `scripts/query_llms.py` with the user's prompt (and optionally a file) to get perspectives from both ChatGPT and Gemini
2. **Analyze responses**: Review what each model suggests, identifying valuable insights, alternative approaches, and potential concerns
3. **Synthesize plan**: Create an implementation plan that incorporates the best ideas from all three models (Claude's own analysis + ChatGPT + Gemini)
4. **Present to user**: Show the final plan along with a brief summary of key contributions from each model

### File-Based Queries

When the user wants the council to review a file (code, schema, config, document):

1. The file will be available at a known path in the sandbox (e.g. mounted via the Files API, or present in the working directory)
2. Pass it to the script using `--file`:
   ```
   python3 scripts/query_llms.py "Review this code for issues" --file /path/to/file.py
   ```
3. The script appends the file content to the prompt under a clearly labeled header
4. Both ChatGPT and Gemini receive the full file content alongside the question

**Trigger phrases that include files:**
- "Consult the council about this file: ..."
- "Ask ChatGPT and Gemini to review [filename]"
- "Get council feedback on my [schema/code/config]"
- "Have the council look at this [file/document]"

## Setup Requirements

The skill requires API keys and optional model configuration stored in a `.env` file in the working directory:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Optional: Specify which models to use (defaults shown below)
OPENAI_MODEL=gpt-5-nano
GEMINI_MODEL=gemini-3-flash-preview
```

**Default Models:**
- ChatGPT: `gpt-5-nano` (fastest, most cost-efficient - $0.05/1M input, $0.40/1M output)
- Gemini: `gemini-3-flash-preview` (balanced speed and intelligence)

**Upgrade Options for Better Collaboration:**

*OpenAI models (ordered by capability and cost):*
- `gpt-5-nano` - Fastest, most cost-efficient ($0.05/1M in, $0.40/1M out) - **DEFAULT**
- `gpt-5-mini` - Faster, cost-efficient for well-defined tasks ($0.25/1M in, $2.00/1M out)
- `gpt-5.2` - Best for coding and agentic tasks ($1.75/1M in, $14.00/1M out)
- `gpt-5.2-pro` - Smarter, more precise for complex problems ($21.00/1M in, $168.00/1M out)

All models support reasoning tokens, 400K context window, and image input.

*Gemini models (ordered by capability):*
- `gemini-2.5-flash-lite` - Ultra-fast, optimized for throughput
- `gemini-2.5-flash` - Best price-performance, large-scale processing
- `gemini-3-flash-preview` - Balanced speed and frontier intelligence (default)
- `gemini-3-pro-preview` - Most intelligent multimodal model, best for complex reasoning

Higher-tier models provide more sophisticated analysis but cost more per API call.

If the `.env` file doesn't exist or keys are missing, inform the user and provide setup instructions.

## Usage Examples

### Example 1: Microservices Architecture

**User input:** "Consult the council: How should I architect a microservices system?"

**Claude's process:**
1. Execute: `python3 scripts/query_llms.py "How should I architect a microservices system?"`
2. Parse JSON responses from ChatGPT and Gemini
3. Analyze their suggestions and synthesize with Claude's own analysis
4. Present the adapted plan with attribution

**Sample synthesized output:**

> Based on consultation with ChatGPT and Gemini, here's the recommended microservices architecture:
>
> **Service Decomposition** — ChatGPT emphasized decomposing by business capability (not technical function), recommending Domain-Driven Design (DDD) as the primary decomposition strategy. Gemini echoed this and added the importance of defining bounded contexts before drawing service boundaries.
>
> **Communication patterns** — Both models agreed on using async messaging (e.g., Kafka or RabbitMQ) for event-driven workflows and synchronous REST/gRPC only for real-time queries. Gemini specifically warned against chatty synchronous chains across more than 2 hops.
>
> **Data isolation** — ChatGPT strongly recommended the Database-per-Service pattern; Gemini suggested starting with logical isolation (separate schemas) before full physical separation to reduce operational overhead early on.
>
> **Observability** — Both recommended distributed tracing (OpenTelemetry), centralized logging, and a service mesh (Istio or Linkerd) once the service count exceeds ~5.
>
> **Key contributions:**
> - ChatGPT: DDD decomposition strategy, API gateway pattern, circuit breaker with Resilience4j
> - Gemini: bounded context warnings, phased data isolation approach, service mesh timing advice

---

### Example 2: Database Design

**User input:** "Ask ChatGPT and Gemini what they think about my database design"

**Claude's process:**
1. Execute: `python3 scripts/query_llms.py "[paste your schema or describe the design]"`
2. Parse and compare both models' feedback on the schema
3. Synthesize a prioritized list of improvements
4. Present findings with attribution

**Sample synthesized output:**

> After consulting ChatGPT and Gemini on your database design:
>
> **Normalization** — Both flagged potential denormalization in the `orders` table. ChatGPT recommended extracting `shipping_address` into its own table to support address reuse; Gemini agreed but noted that for read-heavy workloads, a controlled denormalization with a materialized view may be preferable.
>
> **Indexing** — ChatGPT suggested composite indexes on `(user_id, created_at)` for the most common query pattern. Gemini added that `status` columns with low cardinality are poor standalone index candidates and work better in composite indexes.
>
> **Key contributions:**
> - ChatGPT: normalization advice, index strategy, foreign key constraints
> - Gemini: read-vs-write tradeoffs, query pattern analysis, partitioning considerations

## Output Format

Present the final implementation plan naturally, mentioning key insights from other models inline where relevant. For example:

"Based on consultation with ChatGPT and Gemini, here's the recommended architecture:

[Implementation plan with inline references like "ChatGPT highlighted the importance of..." or "Gemini suggested..."]

Key contributions:
- ChatGPT: [brief summary]
- Gemini: [brief summary]"

### Example 3: File Review

**User input:** "Consult the council about this file: review my API handler for security issues" (with `api_handler.py` mounted at `/workspace/api_handler.py`)

**Claude's process:**
1. Execute: `python3 scripts/query_llms.py "Review this API handler for security issues" --file /workspace/api_handler.py`
2. Both ChatGPT and Gemini receive the full file content with the question
3. Synthesize security findings from both models with Claude's own analysis

## Error Handling

- If API keys are missing, inform user and provide setup instructions
- If an API call fails, note which model's perspective is unavailable and proceed with available responses
- If both APIs fail, inform user and offer to provide Claude's own analysis without external consultation