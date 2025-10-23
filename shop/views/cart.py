from django.shortcuts import render,redirect
from shop.models import Product
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Cart:
    def __init__(self,request):
        self.session=request.session
        cart=self.session.get('session_key')

        if not cart:
            cart=self.session['session_key']={}

        self.cart=cart

    def add(self,product_id):
        product_id=str(product_id)

        if product_id in self.cart:
            self.cart[str(product_id)]+=1
        else:
            self.cart[product_id]=1

        self.session.modified=True
    
    def get_count(self):
        return len(self.cart.keys())
    
    def get_products(self):
        products=[]
        total_with_discount=0

        for pid , quantity in self.cart.items():
            product=Product.objects.get(id=pid)
            if product.discount>0:
                total=product.discount_price*quantity
            else:
                total=product.price*quantity
            total_with_discount += total

            data={
                "quantity":quantity,
                "product":product,
                "total":total
            }
            products.append(data)

        total_price=0
        for p in products:
            total_price += p['product'].price*p["quantity"]

        data={

            "products":products,
            "total_price":total_price,
            "total_with_discount":total_with_discount,
            "profit":total_price-total_with_discount,
        }

        return data
    
    def remove(self,product_id):
        if str(product_id) in self.cart.keys():
            del self.cart[str(product_id)]

            self.session.modified=True
            return True
        return False
    
    def clear(self):
        self.cart.clear()
        self.session.modified=True

class WishList:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist_session_key')
        if not wishlist:
            wishlist = self.session['wishlist_session_key'] = {}
        self.wishlist = wishlist

    def add(self, product_id):
        product_id = str(product_id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = 1
        self.session.modified = True

    def get_count(self):
        return len(self.wishlist.keys())
    
    def get_products(self):
        products=[]

        for pid in self.wishlist.keys():
            products.append(Product.objects.get(id=pid))
            print(pid)

        return products
    
    def remove(self,product_id):
        if str(product_id) in self.wishlist.keys():
            del self.wishlist[str(product_id)]

            self.session.modified=True
            return True
        return False
    

   
class CartPageView(View):
 def get(self,request,product_id=None):
    cart=Cart(request)
    wishlist=WishList(request)
    products=cart.get_products()

    if Product.objects.filter(id=product_id).exists():
            wishlist.remove(product_id)
            wishlist.session.modified=True
            cart.add(product_id)
            cart.session.modified=True
            return redirect('wishlist')
    
    data={
        'path':"Savatcha",
        "products":products,
        "cart_count":cart.get_count(),
        "wishlist_count":wishlist.get_count()
    }

    return render(request,"shop/cart.html",context=data)
 
 def post(self,request,product_id):
    cart=Cart(request)
    wishlist=WishList(request)
    
    if Product.objects.filter(id=product_id).exists():
        wishlist.remove(product_id)
        wishlist.session.modified=True
        cart.add(product_id)
        cart.session.modified=True

        data={
            "message":"savatga qoshildi",
            "cart_count":cart.get_count()
            }

    return JsonResponse(data)


class WishlistView(View):
    def post(self,request,product_id):
        wishlist=WishList(request)
 
        if Product.objects.filter(id=product_id).exists():
            wishlist.add(product_id)
            wishlist.session.modified=True

        data={
            "message":"savatga qoshildi",
            "wishlist_count":wishlist.get_count()
              }
  
        return JsonResponse(data)


    def get(self,request,product_id=None):

        wishlist=WishList(request)
        cart=Cart(request)

        if Product.objects.filter(id=product_id).exists():
            wishlist.add(product_id)
            wishlist.session.modified=True
    
        data={
            "wish_products":wishlist.get_products(),
            'path':"Sevimlilar",
            "cart_count":cart.get_count(),
            "wishlist_count":wishlist.get_count()
        }
        
        return render(request,"shop/wishlist.html",context=data)


class RemoveCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect("cart")


        
class RemoveWishView(View):
    def get(self,request,product_id):
        wishlist=WishList(request)
        wishlist.remove(product_id)
        return redirect("wishlist")
 

class DetailAddProductView(View):
    def get(self, request, id=None):
        cart = Cart(request)
        if Product.objects.filter(id=id).exists():
            cart.add(id)
            cart.session.modified = True
        return redirect('details', id=id)  # ✅ id qo‘shildi
    
class DetailAddToWishlistView(View):
    def get(self, request, id=None):
        wishlist = WishList(request)
        if Product.objects.filter(id=id).exists():
            wishlist.add(id)
            wishlist.session.modified = True
        return redirect('details', id=id)  # ✅ id qo‘shildi

