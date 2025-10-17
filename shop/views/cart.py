from django.shortcuts import render,redirect
from shop.models import Product
from django.http import JsonResponse

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

        for pid , quantity in self.cart.items():
            product=Product.objects.get(id=pid)
            if product.discount>0:
                total=product.discount_price*quantity
            else:
                total=product.price*quantity

            data={
                "quantity":quantity,
                "product":product,
                "total":total
            }
            products.append(data)


        return products
    
    def remove(self,product_id):
        if str(product_id) in self.cart.keys():
            del self.cart[str(product_id)]

            self.session.modified=True
            return True
        return False


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
    

   
def cart_page(request,product_id):
   cart=Cart(request)
   

   if Product.objects.filter(id=product_id).exists():
       cart.add(product_id)

   return JsonResponse({"message":"savatga qoshildi","cart_count":cart.get_count()})


def add_to_wishlist(request,product_id):
    wishlist=WishList(request)
 
    if Product.objects.filter(id=product_id).exists():
        wishlist.add(product_id)
        
    return JsonResponse({"message":"savatga qoshildi","wishlist_count":wishlist.get_count()})

    
def cart(request):
    cart=Cart(request)
    wishlist=WishList(request)
    products=cart.get_products()
    
    data={
        'path':"Savatcha",
        "products":products,
        "cart_count":cart.get_count(),
        "wishlist_count":wishlist.get_count()
    }

    return render(request,"shop/cart.html",context=data)


def wish_list(request):
    wishlist=WishList(request)
    cart=Cart(request)
   
    data={
        "wish_products":wishlist.get_products(),
        'path':"Sevimlilar",
        "cart_count":cart.get_count(),
        "wishlist_count":wishlist.get_count()
    }

    return render(request,"shop/wishlist.html",context=data)


def remove_item_form_cart(request,product_id):
    cart=Cart(request)
    cart.remove(product_id)
    return redirect("cart")

        
def remove_item_from_wishlist(request,product_id):
    wishlist=WishList(request)
    wishlist.remove(product_id)
    return redirect("wishlist")

