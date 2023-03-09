from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render

from .models import Fund
from .insertData import insertData


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
