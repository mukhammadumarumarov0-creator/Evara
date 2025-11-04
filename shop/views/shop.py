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
from shop.models import Review


class DashboardView(View):
    def get(self,request):
        cart=Cart(request)
        wishlist=WishList(request)
        category=Category.objects.all()
        products=Product.objects.all()

        q=request.GET.get('q')
        if q:
            product=Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
            data={
            'path':"Mahsulotlar",
            "product":product,
            'product_count':len(product),
            'cart_count':cart.get_count(),
            'wishlist_count':wishlist.get_count(),
            }

            return render(request,"shop/shop.html",context=data)

       
        paginator=Paginator(products,8)
        

        page=request.GET.get('page')
        page_products=paginator.get_page(page)
        product_count=len(products)
    
    
        data={
            'path':"Mahsulotlar",
            "product":page_products,
            "products":products,
            "product_count":product_count,
            'category':category,
            "cart_count":cart.get_count(),
            'wishlist_count':wishlist.get_count(),
            }
        

        return render(request,"shop/index.html" ,context=data)


class DetailsView(View):
 def get(self,request,id=None):
    product=get_object_or_404(Product,id=id)
    products=Product.objects.all()
    name=product.name
    cart=Cart(request)
    wishlist=WishList(request)
    reviews=Review.objects.filter(product=product)
    q=request.GET.get('q')
    if q:
        product=Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        data={
        'path':"Mahsulotlar",
        "product":product,
        "products":product,
        'product_count':len(product),
        'cart_count':cart.get_count(),
        'wishlist_count':wishlist.get_count(),
        'reviews':reviews,
        }

        return render(request,"shop/shop.html",context=data)

    data={
       'product':product,
       'products':products,
       "path" : f"Mahsulotlar > {name}",
       "cart_count":cart.get_count(),
       "wishlist_count":wishlist.get_count(),
       'reviews':reviews,

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
       data= {
          "order":i,
          "total_price":i.get_total(),
         
       }
       orders.append(data)
       
    q=request.GET.get('q')
    if q:
        product=Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        data={
        'path':"Mahsulotlar",
        "product":product,
        'product_count':len(product),
        'cart_count':cart.get_count(),
        'wishlist_count':wishlist.get_count(),
        }

        return render(request,"shop/shop.html",context=data)
    
    

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


class Password(View):
    def post(self,request):
        user_id=request.user.id
        current_password=request.POST.get("current_password")
        new_password=request.POST.get("new_password")
        new_password2=request.POST.get("new_password2")

        user=User.objects.get(id=user_id)

        if current_password and new_password and new_password2 and user.check_password(current_password) == True and new_password == new_password2:
            user.set_password(new_password2)
            user.save()
            return redirect('register')
        return redirect('account')


class ReviewView(View):
    def post(self, request, id):
        comment_text = request.POST.get('comment_text')
        username = request.POST.get('username')
        email = request.POST.get('email')

        if comment_text and username and email and id:
            product = Product.objects.get(id=id)
            review = Review(
                comment_text=comment_text,
                username=username,
                email=email,
                product=product
            )
            review.save()
        return redirect('dashboard')




        

        
        




        

      
     
    


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








        
 
