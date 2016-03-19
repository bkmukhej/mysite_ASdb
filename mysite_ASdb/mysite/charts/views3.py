# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from .models import AsCategory
from django import template
from django.http import HttpResponse
import json
import datetime
from django.utils import timezone

from .models import AsCategory, AsOrderDetail, AsProduct, AsOrder
from django.db.models import Sum

from . import analysis

from graphos.sources.simple import SimpleDataSource
from graphos.renderers import morris,gchart


# Create your views here.

def index(request):
    return render(request, 'charts/index.html',{'context_category':'root'})

def get_sub_categories(cat_name):
    if cat_name == "root":
        cat_id = 0
    else: 
        cat_id = AsCategory.objects.get(seo_name=cat_name).category_id
    categories = AsCategory.objects.filter(parent_id=cat_id,category_type=1)
    data = []
    for category in categories:
        data.append(category)
    return data
    
'''def get_master_categories():
    categories = AsCategory.objects.filter(category_type=1,category_level=1)
    data = []
    for category in categories:
        data.append(category)
    return data'''

def google_chart(request):
    return render(request, 'charts/gchart.html')

def get_categories(request):
    input = request.POST.get("input","")
    if request.method!="POST": cat_name = "root";
    elif input == "Filter":
        cat_name= request.POST.get("context_category","")
    else:
        cat_name = input
    categories = get_sub_categories(cat_name)
    return {'categories':categories,'context_category':cat_name}
    
def chart_view(request):
    query = get_categories(request)
    categories = query['categories']
    context_category = query['context_category']
    start_date= request.POST.get("start_date","")
    end_date= request.POST.get("end_date","")
    if (start_date and end_date): order_list=set([str(order.order_id) for order in AsOrder.objects.filter(delivery_date__range=[start_date,end_date])])
    volume_data = []
    value_data = []
    for category_object in categories:
        #module = analysis.Module(category_object)
        category_family = set([category_object.category_id])
        level = category_object.category_level
        while(level<3):
            level += 1
            category_family.update(cat.category_id for cat in AsCategory.objects.filter(parent_id__in=category_family))
        #category_family= list(category_family)
        #category_family2 = [str(cat) for cat in category_family]
        product_family = set([prod.product_id for prod in AsProduct.objects.filter(category_id__in=category_family)])
        if (start_date and end_date): 
            quantity = (AsOrderDetail.objects.filter(product_id__in=product_family,order_id__in=order_list).aggregate(Sum('quantity'))['quantity__sum'])
            value = ((AsOrderDetail.objects.filter(product_id__in=product_family,order_id__in=order_list).aggregate(total = Sum('product_price',field='quantity*product_price')))['total'])
        else: 
            quantity = (AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(Sum('quantity'))['quantity__sum'])
            value = ((AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(total = Sum('product_price',field='quantity*product_price')))['total'])
        #if (start_date and end_date): quantity = float((AsOrderDetail.objects.raw('select *,sum(`quantity`) as sum from `as_order_detail` where `product_id` in (select `product_id` from `as_product` where `category_id` in %s and `order_id` in %s)',[category_family2,order_list]))[0].sum)
        #else: quantity = float((AsOrderDetail.objects.raw('select *,sum(`quantity`) as sum from `as_order_detail` where `product_id` in (select `product_id` from `as_product` where `category_id` in %s)',[category_family2]))[0].sum)
        if quantity==None:
            quantity = 0
        else: quantity = int(quantity)
        if value == None:
            value = 0
        else: value = float(value)
        volume_data.append([category_object.category_name,quantity])
        value_data.append([category_object.category_name,value])
    
    #chart_volume_data=[['Name','Sale Volume share']] + percentage_share(volume_data)
    gchart_volume_data=[['Name','Sale Volume share']] + volume_data
    #chart_value_data=[['Name','Sale Value share']] + percentage_share(value_data)
    gchart_value_data=[['Name','Sale Value share']] + value_data
    #chart_volume_data=[['Name','Sale Volume share']] + [['Grocery',56.97],['Personal Care',17.85],['Medicine',18.51],['Magazines',6.68]]
    #chart_value_data=[['Name','Sale Value share']] + [['Grocery',56.97],['Personal Care',17.85],['Medicine',18.51],['Magazines',6.68]]    
    
    #chart_volume = morris.DonutChart(SimpleDataSource(chart_volume_data), options={'title':'Percentage Share'})
    #chart_value = morris.DonutChart(SimpleDataSource(chart_value_data), options={'title':'Percentage Share'})
    #return render(request, 'charts/morris_chart.html',{'data':categories,'chart_volume':chart_volume,'chart_value':chart_value,'start_date':start_date,'end_date':end_date,'context_category':context_category})
    return render(request, 'charts/gchart.html',{'data':categories,'chart_volume':gchart_volume_data,'chart_value':gchart_value_data,'start_date':start_date,'end_date':end_date,'context_category':context_category})
    
def percentage_share(module_list):
    total = float()
    for module in module_list:
        total += module[1]
    if not(total): return module_list
    for module in module_list:
        module[1] = float("{0:.2f}".format(100*module[1]/total))
    return module_list

