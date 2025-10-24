from django.shortcuts import render,get_object_or_404,redirect
from shop.models import Category,Product,Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shop.views import WishList,Cart
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from shop.forms import ResetForm,ResetPasswordForm
from django.contrib.auth.models import User


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
    cart=Cart(request)
    wishlist=WishList(request)

    data={
       'product':product,
       "path" : f"Mahsulotlar > {name}",
       "cart_count":cart.get_count(),
       "wishlist_count":wishlist.get_count()

       }

    return render(request,"shop/details.html",context=data)


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
    user_id=request.user.id
    orders=[]
    for i in Order.objects.filter(user_id=user_id):
       print(i.get_total())
       data= {
          "order":i,
          "total_price":i.get_total(),
         
       }
       orders.append(data)

    form=ResetForm()
    form1=ResetPasswordForm()
      
    
    data={
       "form":form,
       "orders":orders,
       'path':"Profilim",
       'cart_count':cart.get_count(),
       'wishlist_count':wishlist.get_count(),
    }
    return render(request,"shop/accounts.html",data)
 
 def post(self,request):
        user_id=request.user.id

        form=ResetForm(request.POST)
        form1=ResetPasswordForm(request.POST)


        if form.is_valid():
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')

            user=User.objects.get(id=user_id)
            user.first_name=first_name
            user.last_name=last_name
            user.username=username
            user.save()
            return redirect('dashboard')
        
        else:
            message={
                "path":'Profilim',
                "form":form
            }
            return render(request,"shop/accounts.html",context=message)



        
        




        

      
     
    


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








        
 
