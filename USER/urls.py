from django.urls import path
from . import views

urlpatterns = [
    path('profile/update', views.ProfileView.as_view(), name='profile_page'),
]
