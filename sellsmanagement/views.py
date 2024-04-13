from multiprocessing import context
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import SellsProduct
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from ProductManager.models import Products


def search_sells(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        sellsProduct = SellsProduct.objects.filter(
            name__istartswith=search_str, owner=request.user)|SellsProduct.objects.filter(
            amount__istartswith=search_str, owner=request.user)|SellsProduct.objects.filter(
            date__istartswith=search_str, owner=request.user)

        data = sellsProduct.values()
        return JsonResponse(list(data),safe=False)



        

@login_required(login_url="/authentication/login")
def index(request):
    sells = SellsProduct.objects.filter(owner=request.user)
    paginator= Paginator(sells,5)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)


    context = {
        'sells': sells,
        "page_obj" : page_obj
    }

    return render(request,'Sells/index.html', context)

    

def add_sells(request):
    

    context = {
        
        "values": request.POST
    }
    if request.method == "GET":
        return render(request,'Sells/add_sells.html', context)

    if request.method == "POST":
        name = request.POST['name']
        if not name:
            messages.error(request,"name of the product required")
            return render(request,'Sells/add_sells.html', context)
        qauntity = request.POST['qauntity']
        
        date = request.POST['sells_date']
        amount = request.POST['amount']

        if not amount:
            messages.error(request,"amount of the product required")
            return render(request,'Sells/add_sells.html', context)
        if not qauntity:
            messages.error(request,"amount of the qauntity required")
            return render(request,'Sells/add_sells.html', context)
        owner=request.user
        
        
        existing_product = SellsProduct.objects.filter(name=name, owner=owner).first()

        if existing_product:
            existing_product.qauntity+= int(qauntity)
            existing_product.amount += float(amount)
            existing_product.save()


   
        else:
            SellsProduct.objects.create(
                owner=owner,
                name=name,
                amount=amount,
                qauntity=qauntity,
                date=date)
            
        messages.success(request, f"Sells saved successfully for product '{name}'")
        return redirect("sells")

        

    return render(request,'Sells/add_sells.html',context)

def search_products(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')  
        products = Products.objects.filter(name__icontains=search_query)
        
        
        data = []
        for product in products:
            product_data = {
                'name': product.name,
                
                
            }
            data.append(product_data)
        
        return JsonResponse(data, safe=False)

@login_required(login_url="/authentication/login")
def sells_edit(request,id):
    sellsProduct = SellsProduct.objects.get(pk=id)
    

    context = {
        "sellsProduct":sellsProduct,
        "values":sellsProduct,
        
    }
    if request.method=="GET":
        return render(request, "Sells/edit_sells.html",context)

    if request.method=="POST":

        name = request.POST['name']
        if not name:
            messages.error(request,"name of the product required")
            return render(request,'Sells/edit-sells.html', context)
        qauntity = request.POST['qauntity']
        
        date = request.POST['product_date']
        amount = request.POST['amount']

        if not amount:
            messages.error(request,"amount of the  sells product required")
            return render(request,'Sells/edit-sells.html', context)
        if not qauntity:
            messages.error(request,"amount of the qauntity required")
            return render(request,'Sells/edit-sells.html', context)
   

        
        
        sellsProduct.name=name
        sellsProduct.amount=amount
        sellsProduct.qauntity=qauntity
        
        sellsProduct.date=date
        sellsProduct.save()
        messages.success(request,"The Record updated successfully")
        return redirect("sells")

    return render(request,'Sells/edit-sells.html',context)

 
def delete_sells(request,id):
    
    sellsProduct = SellsProduct.objects.get(pk=id)
    sellsProduct.delete()
    messages.success(request,"Record Removed")
    return redirect("sells")
