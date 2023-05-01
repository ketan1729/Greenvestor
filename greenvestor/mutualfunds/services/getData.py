from django.db.models import Sum, F

from ..models import *

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


def getTopEsgFunds():
    esg_list = Esg.objects.select_related('fund').order_by("-esg_score")
    top_esg = esg_list[:limit].values("fund__short_name", "esg_score", "peer_esg_min", "peer_esg_avg", "peer_esg_max")

    e_list = Esg.objects.select_related('fund').order_by("-env_score")
    top_e = e_list[:limit].values("fund__short_name", "env_score", "peer_env_min", "peer_env_avg", "peer_env_max")

    s_list = Esg.objects.select_related('fund').order_by("-soc_score")
    top_s = s_list[:limit].values("fund__short_name", "soc_score", "peer_soc_min", "peer_soc_avg", "peer_soc_max")

    g_list = Esg.objects.select_related('fund').order_by("-gov_score")
    top_g = g_list[:limit].values("fund__short_name", "gov_score", "peer_gov_min", "peer_gov_avg", "peer_gov_max")

    return [list(top_esg), list(top_e), list(top_s), list(top_g)]


def getTopAssets():
    cash_list = Asset.objects.select_related('fund').values("total", "cash") \
        .annotate(actual_cash=F('total') * F('cash')) \
        .order_by("-actual_cash")
    top_cash = cash_list[:limit].values("fund__short_name", "total", "cash", "stocks", "bonds",
                                        "others", "preferred", "convertible")

    stock_list = Asset.objects.select_related('fund').values("total", "stocks") \
        .annotate(actual_stocks=F('total') * F('stocks')) \
        .order_by("-actual_stocks")
    top_stock = stock_list[:limit].values("fund__short_name", "total", "cash", "stocks", "bonds",
                                          "others", "preferred", "convertible")

    bond_list = Asset.objects.select_related('fund').values("total", "bonds") \
        .annotate(actual_bonds=F('total') * F('bonds')) \
        .order_by("-actual_bonds")
    top_bond = bond_list[:limit].values("fund__short_name", "total", "cash", "stocks", "bonds",
                                        "others", "preferred", "convertible")

    return [list(top_cash), list(top_stock), list(top_bond)]
