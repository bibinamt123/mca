from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pro_id', 'name', 'des', 'price')
    search_fields = ('name', 'des')
    list_filter = ('price',)

