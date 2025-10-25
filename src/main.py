import pandas as pd
from factor_model import estimate_betas, apply_scenario
from pathlib import Path
from datetime import datetime, timedelta

def load_tickers_and_startdate() -> tuple[pd.DataFrame, str]:
    """
    Finds the latest *_positioner.csv in /data, extracts its date, 
    sets start_date = that date - 1 year, and loads date_positioner.csv.
    """
    data_dir = Path(__file__).resolve().parent.parent / "data"

    # find latest portfolio file
    portfolio_files = list(data_dir.glob("*_positioner.csv"))
    if not portfolio_files:
        raise FileNotFoundError("No *_positioner.csv files found in data/")

    def extract_date(path: Path) -> datetime:
        return datetime.strptime(path.stem.split("_")[0], "%Y-%m-%d")

    latest_file = max(portfolio_files, key=extract_date)
    latest_date = extract_date(latest_file)
    start_date = (latest_date - timedelta(days=365)).strftime("%Y-%m-%d")

    return latest_file, start_date


if __name__ == "__main__":
    latest_file, start_date = load_tickers_and_startdate()
    
    print(f"Latest portfolio file: {latest_file}, Start date for analysis: {start_date}")

    positions = pd.read_csv(latest_file, sep=";")
    
    print(positions.head())

    betas = estimate_betas(positions['Kortnamn'].tolist(), start=start_date)
    #scenario_impact = apply_scenario(betas, spx_drop=-0.1, us10y_change=0.02)

    print("Estimated Betas:")
    for ticker, beta in betas.items():
        print(f"{ticker}: {beta}")
