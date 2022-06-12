from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Products
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


def search_product(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        product = Products.objects.filter(
            name__istartswith=search_str, owner=request.user)|Products.objects.filter(
            amount__istartswith=search_str, owner=request.user)|Products.objects.filter(
            date__istartswith=search_str, owner=request.user)|Products.objects.filter(
            category__istartswith=search_str, owner=request.user)

        data = product.values()
        return JsonResponse(list(data),safe=False)



        

@login_required(login_url="/authentication/login")
def index(request):
    products = Products.objects.filter(owner=request.user)
    paginator= Paginator(products,5)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)


    context = {
        'products': products,
        "page_obj" : page_obj
    }

    return render(request,'product/index.html', context)

    

def add_product(request):
    categories = Category.objects.all()

    context = {
        "categories":categories,
        "values": request.POST
    }
    if request.method == "GET":
        return render(request,'product/add_product.html', context)

    if request.method == "POST":
        name = request.POST['name']
        if not name:
            messages.error(request,"name of the product required")
            return render(request,'product/add_product.html', context)
        qauntity = request.POST['qauntity']
        category = request.POST['category']
        date = request.POST['product_date']
        amount = request.POST['amount']

        if not amount:
            messages.error(request,"amount of the product required")
            return render(request,'product/add_product.html', context)
        if not qauntity:
            messages.error(request,"amount of the qauntity required")
            return render(request,'product/add_product.html', context)
   

        Products.objects.create(owner=request.user,name=name,amount=amount,qauntity=qauntity,category=category,date=date)
        messages.success(request,"The product added successfully")
        return redirect("products")

    return render(request,'product/add_product.html',context)

def product_edit(request,id):
    product=Products.objects.get(pk=id)
    categories = Category.objects.all()

    context = {
        "product":product,
        "values":product,
        "categories":categories
    }
    if request.method=="GET":
        return render(request, "product/edit-products.html",context)

    if request.method=="POST":

        name = request.POST['name']
        if not name:
            messages.error(request,"name of the product required")
            return render(request,'product/edit-products.html', context)
        qauntity = request.POST['qauntity']
        category = request.POST['category']
        date = request.POST['product_date']
        amount = request.POST['amount']

        if not amount:
            messages.error(request,"amount of the product required")
            return render(request,'product/edit-products.html', context)
        if not qauntity:
            messages.error(request,"amount of the qauntity required")
            return render(request,'product/edit-products.html', context)
   

        
        product.owner=request.user
        product.name=name
        product.amount=amount
        product.qauntity=qauntity
        product.category=category
        product.date=date
        product.save()
        messages.success(request,"The product updated successfully")
        return redirect("products")

    return render(request,'product/edit-products.html',context)

 
def delete_product(request,id):
    product = Products.objects.get(pk=id)
    product.delete()
    messages.success(request,"Product Removed")
    return redirect("products")
