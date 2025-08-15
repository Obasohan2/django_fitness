from django.contrib import admin
from .models import Product, Category

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name','slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','active')
    list_filter = ('category','active')
    search_fields = ('name','slug','description')
    prepopulated_fields = {"slug": ("name",)}