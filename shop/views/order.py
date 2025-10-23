from django.shortcuts import render,redirect
from shop.models import Product,Order,OrderItem
from django.views.generic import View
from shop.views import Cart,WishList
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.telegram import send_message
from asgiref.sync import async_to_sync


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

        message = (
        f"📦 <b>Yangi buyurtma #{order.id}</b>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.username}\n"
        f"🏠 <b>Manzil:</b> {order.address or 'Ko‘rsatilmagan'}\n"
        f"🗒 <b>Qo‘shimcha:</b> {order.additional or 'Yo‘q'}\n"
        f"📌 <b>Status:</b> {order.status}\n\n"
        f"🛍 <b>Mahsulotlar:</b>\n"
         )

        for item in order.items.all():
            message += f"• {item.product.name} x {item.quantity} = ${int(item.total_price):,}\n"

        message += (
            f"\n💰 <b>Umumiy summa:</b> ${int(order.get_total()):,}\n"
            f"🕓 <b>Sana:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"👉🏻 <a href = 'http://127.0.0.1:8000/admin/shop/order/{order.id}/change/' >Buyurtmani ko'rish uchun </a> 👈🏻"
        )
        async_to_sync(send_message)(message)
        cart.clear()

        return redirect('dashboard')
    




   