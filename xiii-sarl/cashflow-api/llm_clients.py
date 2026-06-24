"""French executive summaries of the XIII SARL cashflow, via OpenAI and Anthropic.

Each function takes the cashflow dataframe produced by `build_cashflow_df`
(app.py) and asks one LLM provider for an independent 3-line French
executive summary based on the cumulative cash position at months 12/24/36.

Requires: pip install openai anthropic
Reads OPENAI_API_KEY / ANTHROPIC_API_KEY from the environment.
"""
import os

import pandas as pd
from anthropic import Anthropic
from openai import OpenAI

SUMMARY_PROMPT_TEMPLATE = (
    "Voici la trésorerie cumulée d'une SARL après 12, 24 et 36 mois : "
    "{m12:.0f}€, {m24:.0f}€, {m36:.0f}€. "
    "Rédige un résumé exécutif en français en exactement 3 lignes, "
    "destiné à un comité d'investissement."
)


def _cumulative_cash_at_months(df: pd.DataFrame) -> tuple[float, float, float]:
    by_month = df.set_index("month")["cumulative_cash"]
    return float(by_month[12]), float(by_month[24]), float(by_month[36])


def openai_generate_summary(df: pd.DataFrame, model: str = "gpt-5-nano") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    m12, m24, m36 = _cumulative_cash_at_months(df)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": SUMMARY_PROMPT_TEMPLATE.format(m12=m12, m24=m24, m36=m36)}
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content


def anthropic_generate_summary(df: pd.DataFrame, model: str = "claude-opus-4-8") -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    m12, m24, m36 = _cumulative_cash_at_months(df)
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[
            {"role": "user", "content": SUMMARY_PROMPT_TEMPLATE.format(m12=m12, m24=m24, m36=m36)}
        ],
    )
    return response.content[0].text
