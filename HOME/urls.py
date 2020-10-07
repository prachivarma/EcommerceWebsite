from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('view-product-info/<str:pk>/', views.product_detail, name='product_detail_page'),
    path('search-items/', views.search_items, name='search_items'),
    path('search/', views.search_result, name='search_results'),
]
