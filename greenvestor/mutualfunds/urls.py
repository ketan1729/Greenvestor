from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    # path('insertRecords/', views.insertRecords, name='insertRecords'),
    path('getTopFundsReturns/', views.getTopFundsReturns, name='getTopFundsReturns'),
    path('getTopCategories/', views.getTopCategories, name='getTopCategories'),
    path('getSafeFunds/', views.getSafeFunds, name='getSafeFunds'),
    path('getUnsafeFunds/', views.getUnsafeFunds, name='getUnsafeFunds'),
    path('getESGFunds/', views.getESGFunds, name='getESGFunds'),
    path('getAssetFunds/', views.getAssetFunds, name='getAssetFunds'),
    path('compareFunds/', views.compareFunds, name='compareFunds'),
    path('predictReturns/', views.predictReturns, name='predictReturns'),
]

urlpatterns += staticfiles_urlpatterns()
