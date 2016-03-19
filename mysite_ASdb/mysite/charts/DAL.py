from views import *
from data_objects import Category


def get_sub_categories(cat_name):
    query = AsCategory.objects.filter(seo_name=cat_name)
    cat_id = query[0].category_id
    categories = AsCategory.objects.filter(parent_id=cat_id)
    data = []
    for category in categories:
        data.append(category)
    return data


def get_categories(request):
    if request.method != "POST":
        categories = get_master_categories()
    else:
        cat_name = request.POST.get("input", "")
        categories = get_sub_categories(cat_name)
    return categories


def get_master_categories():
    categories = AsCategory.objects.filter(category_type=1, category_level=1)
    data = []
    for category in categories:
        data.append(category)
    return data


def chart_data(categories, start_date, end_date):

    if (start_date and end_date):
        order_list = set([str(order.order_id) for order in AsOrder.objects.filter(
            delivery_date__range=[start_date, end_date])])
    volume_data = []
    value_data = []
    for category_object in categories:
        value = 0
        category_family = set([category_object.category_id])
        level = category_object.category_level
        while(level < 3):
            level += 1
            for cat in AsCategory.objects.filter(parent_id__in=category_family):
                category_family.add(cat.category_id)
        product_family = [prod.product_id for prod in AsProduct.objects.filter(
            category_id__in=category_family)]
        if (start_date and end_date):
            quantity = (AsOrderDetail.objects.filter(product_id__in=product_family,
                                                     order_id__in=order_list).aggregate(Sum('quantity'))['quantity__sum'])
            value = ((AsOrderDetail.objects.filter(product_id__in=product_family, order_id__in=order_list).aggregate(
                total=Sum('product_price', field='quantity*product_price')))['total'])
        else:
            quantity = (AsOrderDetail.objects.filter(
                product_id__in=product_family).aggregate(Sum('quantity'))['quantity__sum'])
            #value = ((AsOrderDetail.objects.filter(product_id__in=product_family).aggregate(total = Sum('product_price',field='quantity*product_price')))['total'])

        if quantity == None:
            quantity = 0
        else:
            quantity = int(quantity)
        if value == None:
            value = 0
        else:
            value = float(value)
        volume_data.append([str(category_object.category_name), quantity])
        value_data.append([str(category_object.category_name), value])
    return [['Grocery', 56.97], ['Personal Care', 17.85], ['Medicine', 18.51], ['Magazines', 6.68]], [['Grocery', 56.97], ['Personal Care', 17.85], ['Medicine', 18.51], ['Magazines', 6.68]]
