from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('cart/', views.cart, name='cart'),
    path('cart-item/', views.add_item_to_cart, name='add_to_cart'),
    path('change-quantity/', views.change_quantity),
    path('remove-cart-item/', views.remove_cart_item),
    path('in-cart/', views.is_item_in_cart),
    path('otp-verification/', views.verify_otp, name='otp_verify'),
]
