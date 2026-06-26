def calculate_fundamental_score(info):


score = 0

pe = info.get("trailingPE")
debt = info.get("debtToEquity")
roe = info.get("returnOnEquity")
growth = info.get("revenueGrowth")
margin = info.get("profitMargins")

if pe and pe < 25:
    score += 2

if debt and debt < 100:
    score += 2

if roe and roe > 0.15:
    score += 2

if growth and growth > 0.10:
    score += 2

if margin and margin > 0.10:
    score += 2

return score


def get_company_overview(info):


return {
    "company": info.get("longName"),
    "sector": info.get("sector"),
    "industry": info.get("industry"),
    "country": info.get("country"),
    "employees": info.get("fullTimeEmployees"),
    "website": info.get("website"),
    "market_cap": info.get("marketCap"),
    "pe": info.get("trailingPE"),
    "eps": info.get("trailingEps")
}

