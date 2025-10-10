from django.contrib import admin
from shop.models import Category,Product

admin.site.register([Category])

class ProductAdmin(admin.ModelAdmin):
    model=Product
    exclude=("discount_price",)
    list_display=("name","brand","price","discount_price")
    list_display_links=("name","brand","price","discount_price")
    search_fields=('name',)

admin.site.register(Product,ProductAdmin)