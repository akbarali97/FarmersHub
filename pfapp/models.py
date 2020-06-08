from django.db import models
from datetime import date


class Acctype(models.Model):
    u_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    acctypes = models.CharField(max_length=30)

class Person(models.Model):
    email = models.CharField(max_length=30)
    pwd = models.CharField(max_length=30)
    type = models.CharField(max_length=30)


class user_details(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    phoneno = models.CharField(max_length=13)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)


class User_locations(models.Model):
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    locality = models.CharField(max_length=30)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

class products(models.Model):
    name = models.CharField(max_length=30,unique=True)

class contracts(models.Model):
    product = models.ForeignKey('products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30,null=True)
    quantity = models.IntegerField()
    quantity_unit = models.CharField(max_length=15)
    duration = models.IntegerField()
    duration_unit = models.CharField(max_length=10)
    frequency = models.IntegerField()
    frequency_unit = models.CharField(max_length=10)
    price = models.IntegerField()
    price_unit = models.CharField(max_length=30)
    Person = models.ForeignKey('Person', on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default='available')

class reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewee = models.ForeignKey('Person', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='reviewee')
    review = models.TextField(null=True)
    rating = models.FloatField(null=True)

class overall_rating(models.Model):
    overall_rating_id = models.AutoField(primary_key=True)
    ratee = models.ForeignKey('Person', on_delete=models.CASCADE)
    overall_rating = models.FloatField(null=True)


class contract_orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey('Person', on_delete=models.CASCADE)
    buyer = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='buyer')
    contract = models.ForeignKey('contracts', on_delete=models.CASCADE)
    order_datetime = models.CharField(max_length=40)
    contract_start_date = models.CharField(max_length=40,null=True)
    order_status = models.CharField(max_length=12)

class c_o_payment(models.Model):
    c_o_p_id = models.AutoField(primary_key=True)
    c_o_id = models.ForeignKey('contract_orders', on_delete=models.CASCADE)
    payer = models.ForeignKey('Person', on_delete=models.CASCADE)
    payee = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='payee')
    amount = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30)