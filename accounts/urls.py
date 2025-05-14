from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView
from . import views

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
]

