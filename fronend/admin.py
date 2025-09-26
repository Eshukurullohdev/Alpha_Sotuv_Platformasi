from django.contrib import admin
from .models import Product
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'narx', 'created_at')
    list_filter = ('type',)
    search_fields = ('name', 'tavsif')