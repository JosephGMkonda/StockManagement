from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

   path('',views.index, name="sells"),
   path('add-sells',views.add_sells, name="add-sells"),
   path('edit-sells/<int:id>',views.sells_edit,name="sells_edit"),
   path('sells-delete/<int:id>',views.delete_sells,name="sells-delete"),
   path('search-sells',csrf_exempt(views.search_sells),name="search_sells")

]
