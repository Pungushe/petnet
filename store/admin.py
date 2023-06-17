from django.contrib import admin

from .models import Category, Product, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('title',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
