import click
from datetime import datetime, date
from pathlib import Path
from .io_utils import load_csv, save_outputs
from .compute import analyze_shortages
from .viz import plot_total_by_year, plot_aged_by_year

@click.group()
def main():
    """CLI for THC shortages analysis."""

@main.command("analyze")
@click.option("--input", "input_path", required=True, type=click.Path(exists=True, dir_okay=False),
              help="Path to the CSV file exported from Amazon.")
@click.option("--outdir", default="outputs", type=click.Path(file_okay=False), help="Output directory.")
@click.option("--report-date", default=None, help="Analysis date (YYYY-MM-DD). Defaults to today.")
@click.option("--dayfirst", is_flag=True, default=False, help="Parse dates as day-first (e.g., 08/07/2021 = 8 July 2021).")
@click.option("--excel/--no-excel", default=True, help="Write an Excel report with all tables.")
@click.option("--charts/--no-charts", default=True, help="Save PNG charts.")
def analyze_cmd(input_path, outdir, report_date, dayfirst, excel, charts):
    """
    Run the shortages analysis and write outputs to OUTDIR.
    """
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Parse report date
    if report_date:
        try:
            analysis_date = datetime.strptime(report_date, "%Y-%m-%d").date()
        except ValueError:
            raise click.ClickException("Invalid --report-date; expected YYYY-MM-DD")
    else:
        analysis_date = date.today()

    df = load_csv(Path(input_path), dayfirst=dayfirst)

    results = analyze_shortages(
        df,
        analysis_date=analysis_date,
        qty_col="Quantity Variance Amount",
        due_col="Payment Due Date",
        currency_col="Invoice Currency",
    )

    # Save outputs
    payload = save_outputs(results, outdir=outdir, write_excel=excel)

    # Charts
    if charts:
        if not results["annual"].empty:
            plot_total_by_year(results["annual"], outdir / "fig_total_by_year.png")
        if not results["aged_by_year"].empty:
            plot_aged_by_year(results["aged_by_year"], outdir / "fig_aged_by_year.png")

    click.echo(f"Total Shortage USD: {results['totals']['total_shortage_usd']:.2f}")
    click.echo(f"Outputs written to: {outdir}")
    click.echo(f"Run summary: {payload['run_summary_path']}")

if __name__ == "__main__":
    main()
