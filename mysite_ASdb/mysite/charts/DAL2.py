from views import *
from data_objects import Category

def chart_data(context_category_name,start_date,end_date):

    all_category_list = AsCategory.objects.filter(category_type=1)
    all_product_list = AsProduct.objects.values('category_id','product_id')
    
    context_category = get_category_object(context_category_name,all_category_list)
    context_category.find_children(all_category_list)
       
    #return categories
    chart_categories = context_category.children


    if (start_date and end_date):
        order_list=set([str(order.order_id) for order in AsOrder.objects.filter(delivery_date__range=[start_date,end_date])])

    volume_data = []
    value_data = []
    
    for category_object in chart_categories:
        category_object.find_product_facing_categories(all_category_list)
        category_object.assign_products(all_product_list)
        product_family = category_object.products
        

        if (start_date and end_date): 
            quantity = (AsOrderDetail.objects.filter(product_id__in=product_family,order_id__in=order_list).aggregate(Sum('quantity'))['quantity__sum'])
            value = ((AsOrderDetail.objects.filter(product_id__in=product_family,order_id__in=order_list).aggregate(total = Sum('product_price',field='quantity*product_price')))['total'])
        else: 
            quantity = (AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(Sum('quantity'))['quantity__sum'])
            value = ((AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(total = Sum('product_price',field='quantity*product_price')))['total'])
        
        if quantity == None:
            quantity = 0
        else: quantity = int(quantity)
        if value == None:
        	value = 0
        else: value = float(value)
        volume_data.append([str(category_object.category_name),quantity])
        value_data.append([str(category_object.category_name),value])
    return  volume_data,value_data, chart_categories
    



def get_category_object(context_category, all_category_list):
    if context_category =='root': category = 'root'
    else:
        for category in all_category_list:
            if category.category_name == context_category: break
    father_category = Category(category)
    return father_category
