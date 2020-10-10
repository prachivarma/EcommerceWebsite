from django.urls import path
from . import views

urlpatterns = [
    path('register-shop/', views.CreateSeller.as_view(), name='create_seller'),
    path('main/', views.SellerHomeView.as_view(), name='seller_home'),
]
