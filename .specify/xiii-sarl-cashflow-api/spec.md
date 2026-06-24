# Spec: XIII SARL Cashflow API

## Purpose

A FastAPI service that turns a set of business-plan assumptions (salaries, social charges, mortgage, rental income, event/consulting/art revenue, opex, initial cash) into a 36-month cashflow projection for XIII SARL.

## Trigger

Manual — run `uvicorn app:app --reload` from `xiii-sarl/cashflow-api/` (after `pip install -r requirements.txt`), then call the HTTP endpoint. No Claude Code skill trigger is involved.

## Inputs

`POST /generate_cashflow` with an `Assumptions` JSON body:

| Field | Type | Notes |
|---|---|---|
| `salary_months` | `list[float]` | Monthly total salary expense; shorter than 36 entries → last value carries forward |
| `social_pct` | `float` (0-1) | Social charges as a fraction of salary |
| `mortgage_monthly` | `float` | Fixed monthly mortgage payment |
| `rental_monthly` | `float` | Fixed monthly rental income |
| `events_monthly` | `list[float]` | Dîners/events revenue |
| `consulting_monthly` | `list[float]` | Consulting revenue |
| `art_monthly` | `list[float]` | Art sales/commission revenue |
| `opex_monthly` | `list[float]` | Other operating expenses |
| `initial_cash` | `float` | Starting cash position |

Monthly list values must be non-negative; shorter lists are extended to 36 months by repeating the last value, empty lists default to all zeros.

## Outputs

JSON response:

```json
{
  "csv_b64": "<base64-encoded 36-row CSV>",
  "summary": {"month12": ..., "month24": ..., "month36": ...}
}
```

`summary` reports the cumulative cash position at the end of months 12, 24, and 36. Decoding `csv_b64` gives the full month-by-month breakdown (revenue by stream, cost by category, net cashflow, cumulative cash).

## Key files

- `xiii-sarl/cashflow-api/app.py` — entire implementation: `Assumptions` model, 36-month projection logic, CSV/summary response building
- `xiii-sarl/cashflow-api/requirements.txt` — dependencies
- `xiii-sarl/cashflow-api/README.md` — usage docs (run command, endpoint contract) — kept in sync manually with this spec

## Constraints & non-goals

- Stateless, single-endpoint service — no persistence, no auth, no multi-scenario storage
- Projection horizon is fixed at 36 months; not configurable
- No relation to `xiii-sarl/generate_xiii_presentation.py` (the pitch deck) beyond sharing the parent `xiii-sarl/` directory — they are independent tools with separate specs

## Open questions

- No automated tests cover this service
- No deployment target is defined — it's currently a local-only `uvicorn` service
