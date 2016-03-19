# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AsCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    seo_name = models.CharField(max_length=100)
    category_description = models.CharField(max_length=255)
    parent_id = models.IntegerField()
    category_level = models.IntegerField()
    category_image = models.CharField(max_length=100)
    category_web_icon = models.CharField(max_length=150)
    category_icon = models.CharField(max_length=100)
    category_banner = models.CharField(max_length=100)
    show_on_top = models.IntegerField()
    category_type = models.IntegerField()
    meta_title = models.CharField(max_length=60)
    meta_keyword = models.CharField(max_length=160)
    meta_description = models.CharField(max_length=160)
    sort_order = models.IntegerField()
    employee_id = models.IntegerField()
    status = models.IntegerField()
    show_on = models.IntegerField()
    date_added = models.DateTimeField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'as_category'


class AsOrder(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    order_code = models.CharField(max_length=50)
    server_order_id = models.BigIntegerField()
    retailer_order_id = models.BigIntegerField()
    shopper_address_id = models.BigIntegerField()
    merchant_store_id = models.IntegerField()
    order_source = models.IntegerField()
    delivery_date = models.DateField()
    delivery_time_slot = models.CharField(max_length=50)
    delivery_timing = models.CharField(max_length=100)
    order_timing = models.CharField(max_length=100)
    order_status = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.IntegerField()
    total_discount = models.DecimalField(max_digits=8, decimal_places=2)
    special_discount = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2)
    coupon_code = models.CharField(max_length=20)
    shopper_payment_type_id = models.IntegerField()
    merchant_payment_type_id = models.IntegerField()
    ip_address = models.CharField(max_length=30)
    merchant_store_people_id = models.IntegerField()
    delivery_boy_timing = models.CharField(max_length=100)
    packed_timing = models.CharField(max_length=100)
    dispached_timing = models.CharField(max_length=100)
    delivered_timing = models.CharField(max_length=100)
    customer_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_read = models.IntegerField()
    special_request = models.CharField(max_length=255)
    order_completed = models.IntegerField()
    unique_order_id = models.TextField()
    status = models.CharField(db_column='Status', max_length=255)  # Field name made lowercase.
    jiotxnrefnum = models.CharField(db_column='JioTxnRefNum', max_length=255)  # Field name made lowercase.
    errorcode = models.CharField(db_column='ErrorCode', max_length=255)  # Field name made lowercase.
    responsemsg = models.CharField(db_column='ResponseMsg', max_length=255)  # Field name made lowercase.
    txntimestamp = models.CharField(db_column='TxnTimeStamp', max_length=255)  # Field name made lowercase.
    cardnumber = models.CharField(db_column='CardNumber', max_length=255)  # Field name made lowercase.
    txntype = models.CharField(db_column='TxnType', max_length=255)  # Field name made lowercase.
    cardtype = models.CharField(db_column='CardType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'as_order'


class AsOrderDetail(models.Model):
    order_detail_id = models.BigIntegerField(primary_key=True)
    order_id = models.BigIntegerField()
    product_type = models.IntegerField()
    product_id = models.BigIntegerField()
    merchant_product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.IntegerField()
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    free_product = models.CharField(max_length=100)
    combo_detail_items = models.TextField()
    is_available = models.IntegerField()
    image_name = models.CharField(max_length=200)
    offer_description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'as_order_detail'


class AsProduct(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    brand_id = models.IntegerField()
    category_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    seo_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_short_description = models.CharField(max_length=255)
    hightlight_checkout = models.IntegerField()
    display_as_category = models.IntegerField()
    recommended_product = models.IntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    ean_code = models.CharField(max_length=100)
    aaramshop_code = models.CharField(max_length=100)
    is_featured = models.IntegerField()
    featured_start_date = models.DateField()
    featured_end_date = models.DateField()
    meta_title = models.CharField(max_length=60)
    meta_keyword = models.CharField(max_length=160)
    meta_description = models.CharField(max_length=160)
    sort_order = models.IntegerField()
    added_by = models.IntegerField()
    employee_id = models.IntegerField()
    status = models.IntegerField()
    edit_delete = models.IntegerField()
    show_on = models.IntegerField()
    date_added = models.DateTimeField()
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'as_product'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
