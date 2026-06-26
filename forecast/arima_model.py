import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def run_arima_forecast(
        close,
        order=(5,1,0),
        periods=252):

    log_prices = np.log(close)

    model = ARIMA(
        log_prices,
        order=order
    )

    fit = model.fit()

    forecast = (
        fit
        .get_forecast(
            steps=periods
        )
        .predicted_mean
    )

    return np.exp(forecast)