import yfinance as yf
import pandas as pd
import statsmodels.api as sm

def estimate_betas(tickers, start):
    data = yf.download(tickers + ["^GSPC", "^TNX"], start=start)["Adj Close"]
    rets = data.pct_change().dropna()
    X = sm.add_constant(rets[["^GSPC", "^TNX"]])

    betas = {}
    for t in tickers:
        y = rets[t]
        model = sm.OLS(y, X).fit()
        betas[t] = model.params.to_dict()
    return betas

def apply_scenario(betas, spx_drop, us10y_change):
    impact = {}
    for t, b in betas.items():
        impact[t] = b["^GSPC"] * spx_drop + b["^TNX"] * us10y_change
    return pd.Series(impact, name="expected_return")