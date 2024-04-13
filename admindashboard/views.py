from django.shortcuts import render
from django.http import HttpResponse
from ProductManager.models import Products,Category
from sellsmanagement.models import SellsProduct
from django.db.models import Sum
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/authentication/login")
def DashBoard(request):
    


    return render( request,"dashboard/dashboard.html")
@login_required(login_url="/authentication/login")
def product_summary_amount(request):
    categories = Category.objects.all()
    category_summary = {}

    for category in categories:
        products = Products.objects.filter(owner=request.user,category=category)
        total_price = sum(product.total_price for product in products)
        category_summary[category.name] = total_price
    return JsonResponse({"category_summary" : category_summary}, safe=False)

def category_quantity_summary(request):
    categories = Category.objects.all()
    category_summary = {}
    for category in categories:
        total_quantity = Products.objects.filter(owner=request.user,category=category).aggregate(Sum('qauntity'))['qauntity__sum']
        category_summary[category.name] = total_quantity
    return JsonResponse({"category_summary" :category_summary}, safe=False)
