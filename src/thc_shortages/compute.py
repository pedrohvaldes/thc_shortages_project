from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
import pandas as pd
from datetime import date

@dataclass(frozen=True)
class AnalysisContext:
    analysis_date: date
    dayfirst: bool
    columns: tuple
    notes: str = ""

def _ensure_currency_uniform(df: pd.DataFrame, currency_col: str) -> str:
    if currency_col not in df.columns:
        return "Currency column not found."
    vals = df[currency_col].dropna().astype(str).str.upper().unique().tolist()
    if len(vals) == 0:
        return "No currency values found."
    if len(vals) > 1:
        return f"WARNING: Multiple currencies detected: {vals}"
    if vals[0] != "USD":
        return f"WARNING: Currency is {vals[0]}, not USD."
    return "OK"

def analyze_shortages(
    df: pd.DataFrame,
    analysis_date: date,
    qty_col: str = "Quantity Variance Amount",
    due_col: str = "Payment Due Date",
    currency_col: str = "Invoice Currency",
) -> Dict[str, object]:
    """Compute shortage totals, annual breakdown, and aged split.

    Returns a dict with:
      - rows: filtered shortage rows with aging columns
      - annual: totals by year
      - aged_by_year: aged totals by year
      - current_vs_aged: pivot of current vs aged
      - totals: dict with scalar totals
      - context: metadata
    """
    cols_note = _ensure_currency_uniform(df, currency_col)

    # Coerce numeric
    if qty_col not in df.columns:
        raise KeyError(f"Missing column: {qty_col}")
    qty = pd.to_numeric(df[qty_col], errors="coerce").fillna(0.0)

    # Payment due date
    if due_col not in df.columns:
        raise KeyError(f"Missing column: {due_col}")
    due = pd.to_datetime(df[due_col], errors="coerce")

    data = df.copy()
    data["Shortage_Amount"] = qty
    data["Payment_Due_Date"] = due

    # Keep only positive shortages
    data = data.loc[data["Shortage_Amount"] > 0].copy()

    # Aging
    data["days_past_due"] = (pd.Timestamp(analysis_date) - data["Payment_Due_Date"]).dt.days
    data["age_bucket"] = np.where(
        data["days_past_due"] > 90, "Aged (>90 days past due)",
        np.where(
            (data["days_past_due"] >= 0) & (data["days_past_due"] <= 90),
            "Current (0–90 days past due)",
            "Not yet due (negative)",
        ),
    )
    data["Year"] = data["Payment_Due_Date"].dt.year

    # Aggregations
    total_shortage = float(data["Shortage_Amount"].sum())
    shortage_lines = int((data["Shortage_Amount"] > 0).sum())

    annual = (data.groupby("Year")
              .agg(Shortage_Total_USD=("Shortage_Amount", "sum"),
                   Shortage_Count=("Shortage_Amount", "size"),
                   Shortage_Avg_USD=("Shortage_Amount", "mean"))
              .reset_index()
              .sort_values("Year"))

    aged = (data.loc[data["age_bucket"] == "Aged (>90 days past due)"]
            .groupby("Year")
            .agg(Aged_Shortage_USD=("Shortage_Amount", "sum"),
                 Aged_Count=("Shortage_Amount", "size"))
            .reset_index()
            .sort_values("Year"))

    split = (data.loc[data["age_bucket"].isin(["Current (0–90 days past due)","Aged (>90 days past due)"])]
             .pivot_table(index="Year", columns="age_bucket",
                          values="Shortage_Amount", aggfunc="sum", fill_value=0.0)
             .reset_index())

    context = AnalysisContext(
        analysis_date=analysis_date,
        dayfirst=False,  # The loader handles this; we record False/True if you pass it through from CLI
        columns=tuple(df.columns),
        notes=cols_note,
    )

    return {
        "rows": data,
        "annual": annual,
        "aged_by_year": aged,
        "current_vs_aged": split,
        "totals": {
            "total_shortage_usd": total_shortage,
            "shortage_lines": shortage_lines,
        },
        "context": context.__dict__,
    }
