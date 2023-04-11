import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .services.insertData import insertData
from .services.getData import *
from .models import Fund


def index(request):
    latest_fund_list = Fund.objects.order_by('-inception_date')[:5]
    template = loader.get_template('mutualfunds/index.html')
    context = {
        'latest_fund_list': latest_fund_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    return render(request, 'mutualfunds/detail.html', {'fund': fund})


def insertRecords(request):
    insertData()
    return HttpResponse("Data Insertion Completed")


def getTopFundsReturns(request):
    data = getTopFundsAsPerReturns()
    return JsonResponse(data, safe=False)


def getTopCategories(request):
    data = getTopRatedCategories()
    return JsonResponse(data, safe=False)


def getSafeFunds(request):
    data = getTopSafeFunds()
    return JsonResponse(data, safe=False)


def getUnsafeFunds(request):
    data = getTopUnsafeFunds()
    return JsonResponse(data, safe=False)
