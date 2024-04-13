from django.urls import path
from .views import DashBoard
from . import views
urlpatterns = [
    path('', DashBoard, name='dashboard'),
    path('product_summary_amount',views.product_summary_amount,name="product_summary_amount"),
    path('category_quantity_summary',views.category_quantity_summary,name="category_quantity_summary"),
]
