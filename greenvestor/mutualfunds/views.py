import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .services.insertData import insertData
from .services.getData import *
from .models import Fund


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
    base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "returns_data": data_ret,
        "header": header,
        "base_img": base_img
    }
    return render(request, 'mutualfunds/returns.html', {'data':data})


def getTopCategories(request):
    # data = getTopRatedCategories()
    # return JsonResponse(data, safe=False)
    data_cat = getTopRatedCategories()
    header = list(data_cat[0].keys())
    base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "categories_data": data_cat,
        "header": header,
        "base_img": base_img
    }
    return render(request, 'mutualfunds/categories.html', {'data': data})


def getSafeFunds(request):
    # data = getTopSafeFunds()
    # return JsonResponse(data, safe=False)
    data_saf = getTopSafeFunds()
    header = list(data_saf[0].keys())
    base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "safe_data": data_saf,
        "header": header,
        "base_img": base_img
    }
    return render(request, 'mutualfunds/safe.html', {'data': data})


def getUnsafeFunds(request):
    # data = getTopUnsafeFunds()
    # return JsonResponse(data, safe=False)
    data_uns = getTopUnsafeFunds()
    header = list(data_uns[0].keys())
    base_img = 'mutualfunds/media/OikawaPoster.jpg'
    data = {
        "unsafe_data": data_uns,
        "header": header,
        "base_img": base_img
    }
    return render(request, 'mutualfunds/unsafe.html', {'data': data})
