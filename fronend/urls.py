from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]