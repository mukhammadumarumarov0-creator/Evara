from django.contrib import admin
from shop.models import Category,Product

admin.site.register([Category])

class ProductAdmin(admin.ModelAdmin):
    model=Product
    exclude=("discount_price",)

admin.site.register(Product,ProductAdmin)