from django.contrib import admin
from .models import Store, Category, Product, ProductPrice, Profile, ShoppingCart, SavedResult


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 0 # išjungia papildomas tuščias eilutes įvedimui
    fields = ['product', 'price']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'price', 'cart']
    list_filter = ['product', 'store', 'price']


class SavedResultAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'price', 'cart', 'user']
    # list_filter = ['name', 'store', 'cart']


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['date', 'user']
    inlines = [ProductPriceInline]
    readonly_fields = ['date']

admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(Profile)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(SavedResult, SavedResultAdmin)