import numpy as np

def calculate_risk_metrics(close):

    returns = close.pct_change().dropna()

    sharpe = (
        returns.mean()
        /
        returns.std()
    ) * np.sqrt(252)

    rolling_max = close.cummax()

    drawdown = (
        close
        -
        rolling_max
    ) / rolling_max

    max_drawdown = drawdown.min()

    var95 = np.percentile(
        returns,
        5
    )

    return {
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "var95": var95
    }