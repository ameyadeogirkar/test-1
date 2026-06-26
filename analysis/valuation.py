def graham_intrinsic_value(eps, growth):


    if eps is None or growth is None:
        return None

    return eps * (8.5 + (2 * growth * 100))


def dcf_valuation(
free_cash_flow,
growth_rate=0.08,
discount_rate=0.10,
terminal_growth=0.02):


    if free_cash_flow is None:
        return None

    pv = 0

    fcf = free_cash_flow

    for year in range(1, 6):

        fcf *= (1 + growth_rate)

        pv += fcf / ((1 + discount_rate) ** year)

    terminal_value = (
        fcf * (1 + terminal_growth)
    ) / (
        discount_rate - terminal_growth
    )

    pv += (
        terminal_value
        /
        ((1 + discount_rate) ** 5)
    )

    return pv


def valuation_status(
intrinsic_value,
current_price):


    if intrinsic_value is None:
        return "N/A"

    gap = (
        (intrinsic_value-current_price)
        /
        current_price
    ) * 100

    if gap > 15:
        return "Undervalued"

    elif gap < -15:
        return "Overvalued"

    return "Fairly Valued"

