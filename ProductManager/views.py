from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'product/index.html')

def add_product(request):
    return render(request,'product/add_product.html')