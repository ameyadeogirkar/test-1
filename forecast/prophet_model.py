from prophet import Prophet

def run_prophet_forecast(
        df,
        periods=252):

    prophet_df = (
        df["Close"]
        .reset_index()
    )

    prophet_df.columns = [
        "ds",
        "y"
    ]

    model = Prophet()

    model.fit(prophet_df)

    future = model.make_future_dataframe(
        periods=periods
    )

    forecast = model.predict(
        future
    )

    return forecast