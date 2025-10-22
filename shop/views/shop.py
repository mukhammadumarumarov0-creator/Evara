from django.shortcuts import render,get_object_or_404,redirect
from shop.models import Category,Product,Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shop.views import WishList,Cart
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View



class DashboardView(View):
    def get(self,request):

        category=Category.objects.all()
        product=Product.objects.all()

        q=request.GET.get("q")
        if q:
            product=Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        

        paginator=Paginator(product,4)
        cart=Cart(request)
        wishlist=WishList(request)

        page=request.GET.get('page')
        page_products=paginator.get_page(page)
        product_count=len(product)
    
    
        data={
            'path':"Mahsulotlar",
            "product":page_products,
            "product_count":product_count,
            'category':category,
            "cart_count":cart.get_count(),
            'wishlist_count':wishlist.get_count(),
            }
        

        return render(request,"shop/index.html" ,context=data)

class DetailsView(LoginRequiredMixin,View):
 def get(self,request,id):
    product=get_object_or_404(Product,id=id)
    name=product.name

    return render(request,"shop/details.html",context={'product':product,"path" : f"Mahsulotlar > {name}"})


class ShopView(View):
    def get(self,request):
        product=Product.objects.all()
        q=request.GET.get('q')
        if q:
            product=Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

        paginator=Paginator(product,4)
        cart=Cart(request)
        wishlist=WishList(request)

        page=request.GET.get('page')
        page_products=paginator.get_page(page)

        data={
            'path':"Mahsulotlar",
            "product":page_products,
            'product_count':len(product),
            'cart_count':cart.get_count(),
            'wishlist_count':wishlist.get_count(),
            }
        
        return render(request,"shop/shop.html" ,context=data)


class AccountView(View):
 def get(self,request):
    cart=Cart(request)
    wishlist=WishList(request)
    user=request.user.id
    print("bu id",user)
    self.get_my_orders(user)
    
    data={
       
       'path':"Profilim",
       'cart_count':cart.get_count(),
       'wishlist_count':wishlist.get_count(),
    }
    return render(request,"shop/accounts.html",data)

 def get_my_orders(self,user_id):
     
    orders=Order.objects.filter(user_id=user_id)
    for order in orders:
       pass
      
     
    


class SelectedItemsView(View):
    def get(self,request,category_id):
        products=Product.objects.filter(category_id=category_id)
        category=get_object_or_404(Category,id=category_id)

        data={
            "product":products,
            "path":category.name,
            'product_count':len(products),
            }
        
        return render(request,'shop/selected_items.html',context=data)








        
 
