from django.db.models import Sum

from ..models import Fund, Other

limit = 10


def getTopFundsAsPerReturns():
    latest_fund_list = Fund.objects.order_by('-yeartodate_return')[:limit] \
        .values("id", "inception_date", "long_name", "management_name",
                "management_start_date", "short_name", "symbol", "yeartodate_return", "category", "fund_yield",
                "family")
    return list(latest_fund_list)


def getTopRatedCategories():
    category_list = Fund.objects.values("category").annotate(total_return=Sum("yeartodate_return")) \
        .order_by("-total_return")
    top_categories = category_list[:limit].values("category", "total_return")
    return list(top_categories)


def getTopSafeFunds():
    fund_list = Other.objects.select_related('fund').order_by("-sharpe_ratio")
    top_funds = fund_list[:limit].values("fund__short_name", "sharpe_ratio")
    return list(top_funds)


def getTopUnsafeFunds():
    fund_list = Other.objects.select_related('fund').order_by("sharpe_ratio")
    top_funds = fund_list[:limit].values("fund__short_name", "sharpe_ratio")
    return list(top_funds)
