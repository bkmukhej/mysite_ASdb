# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from models import AsCategory
from django import template
from django.http import HttpResponse
import json
from django.db import connection

from .models import AsCategory, AsOrderDetail, AsProduct
from django.db.models import Sum

from analysis import *
from DAL import *
import DAL2
from data_objects import *
from charts import *


# Create your views here.

def google_chart(request):
    return render(request, 'charts/gchart.html')


def chart_view(request):
    if request.method != "POST":
        context_category = "root"
    else:
        context_category = request.POST.get("context_category", "")
    start_date = request.POST.get("start_date", "")
    end_date = request.POST.get("end_date", "")

    volume_data,value_data,categories = DAL2.chart_data(context_category, start_date, end_date)
    #volume_data = value_data = [['Grocery',56.97],['Personal Care',17.85],['Medicine',18.51],['Magazines',6.68]]
    queries = connection.queries
    #return HttpResponse(queries)
    ''' morris_chart_volume = morris_chart(percentage_share(volume_data),'Percentage Share')
    morris_chart_value = morris_chart(percentage_share(value_data),'Percentage Share')
    return render(request, 'charts/morris_chart.html',{'data':categories,'chart_volume':morris_chart_volume,'chart_value':morris_chart_value})'''

    google_chart_volume = gchart(volume_data, 'Percentage Share')
    google_chart_value = gchart(value_data, 'Percentage Share')
    return render(request, 'charts/gchart.html', {'data': categories, 'chart_volume': google_chart_volume, 'chart_value': google_chart_value,'context_category':context_category})


def percentage_share(module_list):
    total = float()
    for module in module_list:
        total += module[1]
    if total == 0:
        return module_list
    for module in module_list:
        module[1] = float("{0:.2f}".format(100 * module[1] / total))
    return module_list
