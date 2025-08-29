import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def plot_total_by_year(annual: pd.DataFrame, outpath: Path) -> None:
    years = annual["Year"].astype(str)
    vals = annual["Shortage_Total_USD"]
    plt.figure()
    plt.bar(years, vals)
    plt.title("Total Shortages by Year (USD)")
    plt.xlabel("Year")
    plt.ylabel("Shortage Total (USD)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

def plot_aged_by_year(aged: pd.DataFrame, outpath: Path) -> None:
    years = aged["Year"].astype(str)
    vals = aged["Aged_Shortage_USD"]
    plt.figure()
    plt.bar(years, vals)
    plt.title("Aged Shortages by Year (USD)")
    plt.xlabel("Year")
    plt.ylabel("Aged Shortage Total (USD)")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
