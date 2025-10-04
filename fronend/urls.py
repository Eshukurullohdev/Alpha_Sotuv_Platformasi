from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path("admin-page/", admin_page, name="admin_page"),
    path("admin-page/edit/<int:pk>/", edit_product, name="edit_product"),
    path("admin-page/delete/<int:pk>/", delete_product, name="delete_product"),
    path("admin-page/profile/", profile_view, name="profile"),
    path("admin-page/dashboard/", dashboard, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-logout/', admin_logout, name='admin_logout'),
]