from django.urls import path
from . import views

urlpatterns = [
    path('list-product/', views.ListProductView.as_view(), name='list_product'),
    path('inventory/', views.InventoryListView.as_view(), name='inventory_page'),
]
