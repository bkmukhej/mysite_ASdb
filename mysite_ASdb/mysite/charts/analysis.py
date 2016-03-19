# -*- coding: utf-8 -*-
from .models import AsCategory, AsOrderDetail, AsProduct,AsOrder
from django.db.models import Sum
from views import *


'''class Module():
    def __init__(self, category_object):
        self.name = category_object.category_name
        category_family = [category_object.category_id]
        level = category_object.category_level
        while(level<3):
            level += 1
            for cat in AsCategory.objects.filter(parent_id__in=category_family):
                category_family.append(cat.category_id)
        product_family = [prod.product_id for prod in AsProduct.objects.filter(category_id__in=category_family)]
        
        self.quantity = int(AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(Sum('quantity'))['quantity__sum'])
        #self.value_share = sum(order_value)'''


def chart_data(categories,start_date,end_date):

    if (start_date and end_date): order_list=set([str(order.order_id) for order in AsOrder.objects.filter(delivery_date__range=[start_date,end_date])])
    volume_data = []
    value_data = []
    for category_object in categories:
        
        category_family = [category_object.category_id]
        level = category_object.category_level
        while(level<3):
            level += 1
            for cat in AsCategory.objects.filter(parent_id__in=category_family):
                category_family.append(cat.category_id)
        product_family = [prod.product_id for prod in AsProduct.objects.filter(category_id__in=category_family)]
        quantity = AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(Sum('quantity'))['quantity__sum']
        queries = connection.queries
        #return HttpResponse(str(queries))
        if quantity == None:
            quantity = 0
        else: quantity = int(quantity)
        volume_data.append([str(category_object.category_name),quantity])
        #value_data.append([category_object.category_name,module.value_share])
    return  volume_data,value_data
    
    