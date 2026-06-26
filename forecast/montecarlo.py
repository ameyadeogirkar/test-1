import numpy as np

def monte_carlo_forecast(
        close,
        days=252,
        simulations=1000):

    returns = (
        close
        .pct_change()
        .dropna()
    )

    mu = returns.mean()

    sigma = returns.std()

    current = close.iloc[-1]

    paths = np.zeros(
        (days, simulations)
    )

    paths[0] = current

    for t in range(1, days):

        shock = np.random.normal(
            0,
            1,
            simulations
        )

        paths[t] = (
            paths[t-1]
            *
            np.exp(
                (
                    mu
                    -
                    0.5*sigma**2
                )
                +
                sigma*shock
            )
        )

    return paths