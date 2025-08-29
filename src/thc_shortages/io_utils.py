from pathlib import Path
import pandas as pd
from typing import Dict
from datetime import date
import json

def load_csv(path: Path, dayfirst: bool = False) -> pd.DataFrame:
    """Load CSV with robust defaults and minimal validation."""
    df = pd.read_csv(path, encoding="utf-8", sep=",")
    # Try to infer relevant dates if present
    for col in ["Invoice Date", "Payment Due Date", "Invoice Creation Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=dayfirst)
    return df

def save_outputs(results: Dict, outdir: Path, write_excel: bool = True) -> Dict[str, Path]:
    outdir.mkdir(parents=True, exist_ok=True)

    # Save CSVs
    annual_csv = outdir / "annual_breakdown.csv"
    aged_csv = outdir / "aged_by_year.csv"
    split_csv = outdir / "current_vs_aged.csv"
    results["annual"].to_csv(annual_csv, index=False)
    results["aged_by_year"].to_csv(aged_csv, index=False)
    results["current_vs_aged"].to_csv(split_csv, index=False)

    # Excel report
    report_xlsx = outdir / "shortage_analysis_report.xlsx"
    if write_excel:
        with pd.ExcelWriter(report_xlsx, engine="openpyxl") as writer:
            results["rows"].to_excel(writer, sheet_name="Shortage Rows (Raw)", index=False)
            results["annual"].to_excel(writer, sheet_name="Annual Breakdown", index=False)
            results["aged_by_year"].to_excel(writer, sheet_name="Aged by Year", index=False)
            results["current_vs_aged"].to_excel(writer, sheet_name="Current vs Aged", index=False)

    # Run summary
    run_summary = {
        "analysis_date": results["context"]["analysis_date"].isoformat(),
        "dayfirst": results["context"]["dayfirst"],
        "columns_detected": list(results["context"]["columns"]),
        "total_shortage_usd": round(results["totals"]["total_shortage_usd"], 2),
        "shortage_lines": int(results["totals"]["shortage_lines"]),
        "notes": results["context"]["notes"],
    }
    summary_path = outdir / "run_summary.json"
    summary_path.write_text(json.dumps(run_summary, indent=2))

    return {
        "annual_path": annual_csv,
        "aged_path": aged_csv,
        "split_path": split_csv,
        "report_path": report_xlsx if write_excel else None,
        "run_summary_path": summary_path,
    }
