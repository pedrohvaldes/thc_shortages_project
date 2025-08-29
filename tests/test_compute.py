import pandas as pd
from datetime import date
from thc_shortages.compute import analyze_shortages

def test_basic_aged_logic():
    df = pd.DataFrame({
        "Quantity Variance Amount": [10.0, 20.0, 30.0, 0.0],
        "Payment Due Date": ["2024-01-01", "2024-12-01", "2025-05-01", "2025-05-01"],
        "Invoice Currency": ["USD", "USD", "USD", "USD"],
    })
    res = analyze_shortages(df, analysis_date=date(2025, 8, 29))
    total = res["totals"]["total_shortage_usd"]
    assert round(total, 2) == 60.0  # ignores the zero shortage
    aged = res["aged_by_year"].set_index("Year")["Aged_Shortage_USD"].to_dict()
    # As of 2025-08-29, everything here is aged
    assert aged[2024] == 30.0  # 10 + 20 in 2024
    assert aged[2025] == 30.0  # 30 in 2025
