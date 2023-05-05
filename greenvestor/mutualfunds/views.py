import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .services.insertData import insertData
from .services.getData import *
from .models import Fund
from .forms.comparefunds import CompareFundsForm


def index(request):
    # latest_fund_list = Fund.objects.order_by('-inception_date')[:5]
    # template = loader.get_template('mutualfunds/index.html')
    # context = {
    #     'latest_fund_list': latest_fund_list
    # }
    # return HttpResponse(template.render(context, request))
    return render(request, 'mutualfunds/home.html')


def detail(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    return render(request, 'mutualfunds/detail.html', {'fund': fund})


def insertRecords(request):
    insertData()
    return HttpResponse("Data Insertion Completed")


def getTopFundsReturns(request):
    data_ret = getTopFundsAsPerReturns()
    header = list(data_ret[0].keys())
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "returns_data": data_ret,
        "header": header,
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/returns.html', {'data': data})


def getTopCategories(request):
    # data = getTopRatedCategories()
    # return JsonResponse(data, safe=False)
    data_cat = getTopRatedCategories()
    header = list(data_cat[0].keys())
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "categories_data": data_cat,
        "header": header,
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/categories.html', {'data': data})


def getSafeFunds(request):
    # data = getTopSafeFunds()
    # return JsonResponse(data, safe=False)
    data_saf = getTopSafeFunds()
    header = list(data_saf[0].keys())
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "safe_data": data_saf,
        "header": header,
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/safe.html', {'data': data})


def getUnsafeFunds(request):
    # data = getTopUnsafeFunds()
    # return JsonResponse(data, safe=False)
    data_uns = getTopUnsafeFunds()
    header = list(data_uns[0].keys())
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "unsafe_data": data_uns,
        "header": header,
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/unsafe.html', {'data': data})


def getESGFunds(request):
    esg_data = getTopEsgFunds()
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    header = []
    for d in esg_data:
        header.append(list(d[0].keys()))

    data = {
        'esg_data': esg_data[0],
        'e_data': esg_data[1],
        's_data': esg_data[2],
        'g_data': esg_data[3],
        'esg_header': header[0],
        'e_header': header[1],
        's_header': header[2],
        'g_header': header[3],
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/esg.html', {'data': data})


def getAssetFunds(request):
    asset_data = getTopAssets()
    # base_img = 'mutualfunds/media/OikawaPoster.jpg'
    header = list(asset_data[0][0].keys())

    data = {
        'cash_data': asset_data[0],
        'stock_data': asset_data[1],
        'bond_data': asset_data[2],
        'header': header,
        # "base_img": base_img
    }
    return render(request, 'mutualfunds/asset.html', {'data': data})


def compareFunds(request):
    comp_obj = {}
    if request.method == "POST":
        compare_funds_form = CompareFundsForm(request.POST)
        comp_obj["form"] = compare_funds_form

        if compare_funds_form.is_valid():
            funds = compare_funds_form.data["funds"]
            cf_data = getFundsComparison(funds)

            x = []
            y = []
            ret_data = {}
            labels_list = []
            for ro in cf_data["returns_comp"]:
                if ro['fund__symbol'] not in ret_data:
                    ret_data[ro['fund__symbol']] = {"x": [], "y": []}
                    labels_list.append(ro['fund__symbol'])

                ret_data[ro['fund__symbol']]["y"].append(ro["value"])
                ret_data[ro['fund__symbol']]["x"].append(str(ro["year"]) + "-" + str(ro["quarter"]))

            for key in ret_data:
                x.append(ret_data[key]["x"])
                y.append(ret_data[key]["y"])

            comp_obj["returns_plot"] = {"x": x, "y": y, "title": "Returns Values", "symbols": labels_list}

            x = []
            y = []
            for eo in cf_data["esg_comp"]:
                x.append(eo["fund__symbol"])
                y.append(eo["esg_score"])

            comp_obj["esg_plot"] = {"x": x, "y": y, "title": "ESG Comparison"}

            x = []
            y = []
            for eo in cf_data["asset_comp"]:
                x.append(eo["fund__symbol"])
                y.append(eo["total"])

            comp_obj["asset_plot"] = {"x": x, "y": y, "title": "Assets Comparison"}

            x = []
            y_sharpe = []
            y_treynor = []
            y_mar = []
            for eo in cf_data["other_comp"]:
                x.append(eo["fund__symbol"])
                y_sharpe.append(eo["sharpe_ratio"])
                y_treynor.append(eo["treynor_ratio"])
                y_mar.append(eo["mean_annual_return"])

            comp_obj["other_plot"] = {"x": x, "y": [y_sharpe, y_treynor, y_mar], "title": "Assets Comparison"}
    else:
        compare_funds_form = CompareFundsForm()
        comp_obj = {
            "form": compare_funds_form
        }
    return render(request, 'mutualfunds/comparefunds.html', {'data': comp_obj})
