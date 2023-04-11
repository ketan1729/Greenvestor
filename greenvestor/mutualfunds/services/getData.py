from ..models import Fund


def getTopFundsAsPerReturns():
    latest_fund_list = Fund.objects.order_by('-yeartodate_return')[:5]\
        .values("id", "inception_date", "investment_strategy", "long_name", "management_bio", "management_name",
                "management_start_date", "short_name", "symbol", "yeartodate_return", "category", "fund_yield",
                "family")
    return list(latest_fund_list)
