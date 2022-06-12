from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

   path('',views.index, name="products"),
   path('add-product',views.add_product, name="add-products"),
   path('edit-product/<int:id>',views.product_edit,name="product_edit"),
   path('product-delete/<int:id>',views.delete_product,name="product-delete"),
   path('search-product',csrf_exempt(views.search_product),name="search_product")

]
