from django.urls import path
from . import views

urlpatterns = [

   path('',views.index, name="products"),
   path('add-product',views.add_product, name="add-products")

]
