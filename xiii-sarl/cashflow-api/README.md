# XIII SARL Cashflow API

FastAPI service that turns a set of business-plan assumptions into a 36-month
cashflow projection.

## Run

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Endpoint

`POST /generate_cashflow`

Body (`Assumptions`):

| Field | Type | Notes |
|---|---|---|
| `salary_months` | `list[float]` | Monthly total salary expense. Shorter than 36 entries → last value carries forward. |
| `social_pct` | `float` (0-1) | Social charges as a fraction of salary. |
| `mortgage_monthly` | `float` | Fixed monthly mortgage payment. |
| `rental_monthly` | `float` | Fixed monthly rental income. |
| `events_monthly` | `list[float]` | Dîners/events revenue. |
| `consulting_monthly` | `list[float]` | Consulting revenue. |
| `art_monthly` | `list[float]` | Art sales/commission revenue. |
| `opex_monthly` | `list[float]` | Other operating expenses. |
| `initial_cash` | `float` | Starting cash position. |

Monthly list values must be non-negative; shorter lists are extended to 36
months by repeating the last value, empty lists default to all zeros.

Response:

```json
{
  "csv_b64": "<base64-encoded 36-row CSV>",
  "summary": {"month12": ..., "month24": ..., "month36": ...}
}
```

`summary` reports the cumulative cash position at the end of months 12, 24,
and 36. Decode `csv_b64` to get the full month-by-month breakdown (revenue by
stream, cost by category, net cashflow, cumulative cash).
