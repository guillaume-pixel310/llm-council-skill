"""XIII SARL cashflow projection API.

Builds a 36-month cashflow table from a set of business-plan
assumptions and returns it as a base64-encoded CSV plus a short
summary (cumulative cash position at month 12/24/36).

Run with: uvicorn app:app --reload
"""
import base64
from typing import List

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="XIII SARL Cashflow API")

HORIZON_MONTHS = 36


class Assumptions(BaseModel):
    salary_months: List[float] = Field(default_factory=list)
    social_pct: float = Field(ge=0, le=1)
    mortgage_monthly: float = Field(ge=0)
    rental_monthly: float = Field(ge=0)
    events_monthly: List[float] = Field(default_factory=list)
    consulting_monthly: List[float] = Field(default_factory=list)
    art_monthly: List[float] = Field(default_factory=list)
    opex_monthly: List[float] = Field(default_factory=list)
    initial_cash: float

    @field_validator(
        "salary_months", "events_monthly", "consulting_monthly", "art_monthly", "opex_monthly"
    )
    @classmethod
    def no_negative_values(cls, v: List[float]) -> List[float]:
        if any(x < 0 for x in v):
            raise ValueError("monthly values must be non-negative")
        return v


def _extend_to_horizon(values: List[float], horizon: int = HORIZON_MONTHS) -> List[float]:
    """Pad a monthly series out to `horizon` months.

    Shorter series are extended by repeating their last value (so a
    plan can describe a ramp-up phase and have the steady-state value
    carry forward); empty series become all zeros.
    """
    if not values:
        return [0.0] * horizon
    if len(values) >= horizon:
        return list(values[:horizon])
    return list(values) + [values[-1]] * (horizon - len(values))


def build_cashflow_df(a: Assumptions) -> pd.DataFrame:
    salary = _extend_to_horizon(a.salary_months)
    events = _extend_to_horizon(a.events_monthly)
    consulting = _extend_to_horizon(a.consulting_monthly)
    art = _extend_to_horizon(a.art_monthly)
    opex = _extend_to_horizon(a.opex_monthly)

    rows = []
    cumulative_cash = a.initial_cash
    for m in range(1, HORIZON_MONTHS + 1):
        i = m - 1
        revenue_total = events[i] + consulting[i] + art[i] + a.rental_monthly
        cost_social = salary[i] * a.social_pct
        cost_total = salary[i] + cost_social + a.mortgage_monthly + opex[i]
        net_cashflow = revenue_total - cost_total
        cumulative_cash += net_cashflow

        rows.append({
            "month": m,
            "revenue_events": events[i],
            "revenue_consulting": consulting[i],
            "revenue_art": art[i],
            "revenue_rental": a.rental_monthly,
            "total_revenue": revenue_total,
            "cost_salary": salary[i],
            "cost_social": cost_social,
            "cost_mortgage": a.mortgage_monthly,
            "cost_opex": opex[i],
            "total_cost": cost_total,
            "net_cashflow": net_cashflow,
            "cumulative_cash": cumulative_cash,
        })

    return pd.DataFrame(rows)


@app.post("/generate_cashflow")
def generate(a: Assumptions):
    df = build_cashflow_df(a)

    csv_bytes = df.to_csv(index=False).encode()
    csv_b64 = base64.b64encode(csv_bytes).decode()

    by_month = df.set_index("month")["cumulative_cash"]
    summary = {
        "month12": round(float(by_month[12]), 2),
        "month24": round(float(by_month[24]), 2),
        "month36": round(float(by_month[36]), 2),
    }

    return {"csv_b64": csv_b64, "summary": summary}
