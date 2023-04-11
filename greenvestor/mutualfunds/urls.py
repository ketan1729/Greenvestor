from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('insertRecords/', views.insertRecords, name='insertRecords'),
    path('getTopFundsReturns/', views.getTopFundsReturns, name='getTopFundsReturns'),
    path('getTopCategories/', views.getTopCategories, name='getTopCategories'),
    path('getSafeFunds/', views.getSafeFunds, name='getSafeFunds'),
    path('getUnsafeFunds/', views.getUnsafeFunds, name='getUnsafeFunds'),
]
