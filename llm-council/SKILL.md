---
name: llm-council
description: Multi-LLM collaborative brainstorming using MetaGPT-inspired role-based orchestration. Use when user explicitly requests consultation with multiple AI models (ChatGPT, Gemini, other LLMs) before presenting an implementation plan, or asks to "consult the council", "ask the council", "ask ChatGPT and Gemini", "ask other models", or "get perspectives from other AIs". Each external LLM is assigned a functional role—ProductManager (ChatGPT) analyzes requirements first; Architect (Gemini) designs a solution with full visibility into the PM's analysis. Roles execute sequentially so each builds on the prior one's output before Claude synthesizes a final recommendation.
---

# LLM Council

Orchestrate a council of AI agents—each assigned a functional role—where each role's output informs the next, building context progressively, before Claude synthesizes a final recommendation.

## Architecture (MetaGPT Patterns)

```
User prompt
    ↓
ProductManager (ChatGPT) — AnalyzeRequirements
    Sees: user prompt
    Produces: structured requirements analysis (goals, constraints, success criteria)
    ↓ [context accumulated into message history]
Architect (Gemini) — DesignSolution
    Sees: user prompt + ProductManager's requirements analysis
    Produces: concrete technical design (approach, trade-offs, risks, tools)
    ↓
Claude — Synthesis
    Sees: all role outputs
    Produces: integrated recommendation with role attribution
```

This sequential context accumulation is the core MetaGPT pattern: each role receives the full message history so downstream roles genuinely build on upstream outputs rather than responding in parallel.

## Trigger Phrases

When user requests consultation with other AI models, including:
- "Consult the council: [your question]"
- "Consult with ChatGPT and Gemini about..."
- "Ask ChatGPT and Gemini what they think about..."
- "Ask other AI models what they think about..."
- "Get perspectives from the council on..."
- "Consult the LLM council: [your question]"

## Process

1. **Run council**: Execute `python3 scripts/query_llms.py "<user question>"` — this runs both roles sequentially and returns structured JSON
2. **Parse output**: Read `council.productmanager.response` (PM's requirements analysis) and `council.architect.response` (Architect's design, informed by PM)
3. **Read message history**: The `messages` array shows the full context accumulation chain
4. **Synthesize**: Create a recommendation that:
   - Acknowledges what the ProductManager surfaced (requirements, constraints, gaps)
   - Credits the Architect's design decisions (referencing which PM requirements they addressed)
   - Adds Claude's own perspective as a third voice
   - Notes where roles agreed and where they diverged
5. **Present to user**: Show the synthesized plan with role attribution

## Setup Requirements

API keys and optional model configuration in a `.env` file in the working directory:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...

# Optional: override default models
OPENAI_MODEL=gpt-5-nano
GEMINI_MODEL=gemini-3-flash-preview
```

**Default Models:**
- ProductManager (ChatGPT): `gpt-5-nano` — fast, cost-efficient ($0.05/1M input, $0.40/1M output)
- Architect (Gemini): `gemini-3-flash-preview` — balanced speed and frontier intelligence

**Upgrade Options:**

*OpenAI models (ordered by capability):*
- `gpt-5-nano` — fastest, most cost-efficient — **DEFAULT**
- `gpt-5-mini` — efficient for well-defined tasks
- `gpt-5.2` — best for complex reasoning and coding tasks
- `gpt-5.2-pro` — most capable for expert-level analysis

*Gemini models (ordered by capability):*
- `gemini-2.5-flash-lite` — ultra-fast, optimized for throughput
- `gemini-2.5-flash` — best price-performance
- `gemini-3-flash-preview` — balanced speed and frontier intelligence — **DEFAULT**
- `gemini-3-pro-preview` — most capable for complex reasoning

If `.env` doesn't exist or keys are missing, inform the user and provide setup instructions.

## Usage Examples

### Example 1: Database Technology Choice

**User input:** "Consult the council: Should I use PostgreSQL or MongoDB for my SaaS app?"

**Claude's process:**
1. Execute: `python3 scripts/query_llms.py "Should I use PostgreSQL or MongoDB for my SaaS app?"`
2. ProductManager analyzes requirements (e.g., schema flexibility needs, ACID requirements, query patterns, team expertise)
3. Architect receives PM's analysis as context and designs a concrete recommendation (e.g., PostgreSQL with JSONB for hybrid flexibility, specific indexing, migration path)
4. Claude synthesizes both with its own perspective

**Sample synthesized output:**

> I consulted the council — here's the integrated recommendation:
>
> **ProductManager's Requirements Analysis**
> The ProductManager identified three key constraints: your schema will evolve frequently in early stages (favoring flexibility), you need ACID transactions for billing (favoring relational), and your team has stronger SQL experience than NoSQL.
>
> **Architect's Design** (informed by PM's analysis)
> Given those requirements, the Architect recommended PostgreSQL with JSONB columns for flexible fields rather than a pure document store. This preserves ACID guarantees for billing while allowing schema evolution in the JSONB columns without migrations. Specific advice: `GIN` indexes on JSONB for fast queries, `pg_partman` for table partitioning as you scale.
>
> **Claude's synthesis**
> Both roles converged on PostgreSQL but for complementary reasons—PM from requirements, Architect from implementation. I'd add: don't use JSONB as a crutch for every field; keep structured data in proper columns and reach for JSONB only for genuinely variable attributes.
>
> **Key contributions:**
> - ProductManager: surfaced the billing ACID requirement and team SQL expertise
> - Architect: proposed the JSONB hybrid approach and specific indexing strategy

---

### Example 2: Microservices Architecture

**User input:** "Consult the council: How should I architect a microservices system?"

**Claude's process:**
1. Execute: `python3 scripts/query_llms.py "How should I architect a microservices system?"`
2. ProductManager surfaces requirements: team size, deployment frequency, existing monolith vs greenfield, domain complexity
3. Architect designs the service decomposition strategy, communication patterns, and data isolation approach — referencing the PM's requirements in its design
4. Claude synthesizes into a concrete plan

**Sample synthesized output:**

> **ProductManager's Requirements Analysis**
> The PM flagged that "microservices" is often chosen prematurely. Key questions it surfaced: Is the monolith actually painful? How large is the team? What are the deployment requirements?
>
> **Architect's Design** (building on PM's analysis)
> Given the PM's framing, the Architect proposed a "strangler fig" migration path rather than a greenfield rewrite: extract one domain boundary at a time. For communication: async messaging (Kafka) for event-driven workflows, synchronous gRPC only for latency-sensitive queries. For data: start with logical isolation before physical separation.
>
> **Claude's synthesis**
> The PM's analysis changed the Architect's answer in a meaningful way — the Architect addressed migration path rather than assuming greenfield. My addition: don't adopt a service mesh until you have 5+ services.
>
> **Key contributions:**
> - ProductManager: reframed the question around readiness, surfaced team-size and existing system context
> - Architect: strangler fig migration pattern, async-first communication, phased data isolation

## Output Format

Present the synthesized recommendation organized around the role contributions:

```
**ProductManager's Requirements Analysis**
[What the PM surfaced: requirements, constraints, gaps flagged]

**Architect's Design** (building on PM's analysis)
[Architect's technical approach, explicitly referencing PM's requirements it addressed]

**Synthesis** (Claude's perspective)
[Where roles agreed, where they diverged, Claude's own additions]

**Key contributions:**
- ProductManager: [specific insights]
- Architect: [specific insights, noting how it built on PM]
```

## Error Handling

- If OpenAI API fails: note that ProductManager analysis is unavailable; Architect runs with original prompt only (no PM context); note the reduced context in synthesis
- If Gemini API fails: use ProductManager analysis; proceed with Claude's own design perspective
- If both APIs fail: inform user, provide `.env` setup instructions, offer Claude's own analysis
- Never produce empty output — always provide value from whatever is available
