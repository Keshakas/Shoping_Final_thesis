from django.contrib import admin

from .models import Store, Category, Product, ProductPrice


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'price', 'date_checked']
    list_filter = ['product', 'store', 'price']
    readonly_fields = ('date_checked',)

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)