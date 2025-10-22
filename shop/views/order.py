from django.shortcuts import render,redirect
from shop.models import Product,Order,OrderItem
from django.views.generic import View
from shop.views import Cart,WishList
from django.contrib.auth.mixins import LoginRequiredMixin


class GetCheckOutView(LoginRequiredMixin,View):
    def get(self,request):
        cart=Cart(request)
        wishlist=WishList(request)


        products=cart.get_products()

        data={
           "path":"Savatcha",
           "cart_count":cart.get_count(),
           "wishlist_count":wishlist.get_count(),
           "products":products
        }
        
        return render(request,"shop/checkout.html",context=data)
    
    def post(self, request):
        user = request.user
        cart = Cart(request)
        cart_data = cart.get_products()       
        products = cart_data["products"]     

        address = request.POST.get('address')
        additional = request.POST.get('additional')

        items = []

        for item_data in products:
            order_item, created = OrderItem.objects.get_or_create(
                product=item_data['product'],
                quantity=item_data['quantity'],
                total_price=item_data['total']
            )
            items.append(order_item)

        order = Order.objects.create(
            user=user,
            address=address,
            additional=additional
        )

    
        order.items.add(*items)
        cart.clear()
        
        return redirect('dashboard')
    




   