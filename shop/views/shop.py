from django.shortcuts import render,get_object_or_404
from shop.models import Category,Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shop.views import WishList,Cart




   

def dashboard(request):

    category=Category.objects.all()
    product=Product.objects.all()
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


@login_required
def details(request,id):
   product=get_object_or_404(Product,id=id)
   name=product.name

   return render(request,"shop/details.html",context={'product':product,"path" : f"Mahsulotlar > {name}"})


@login_required
def shop(request):
    product=Product.objects.all()
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


@login_required
def accounts(request):
    cart=Cart(request)
    wishlist=WishList(request)
    return render(request,"shop/accounts.html",context={'path':"Profilim",'cart_count':cart.get_count(),'wishlist_count':wishlist.get_count(),})


@login_required
def check_out(request):
    return render(request,"shop/checkout.html")


def selected_items(request,category_id):
    products=Product.objects.filter(category_id=category_id)
    category=get_object_or_404(Category,id=category_id)

    data={
        "product":products,
        "path":category.name,
        'product_count':len(products),
        }
    
    return render(request,'shop/selected_items.html',context=data)








        
 
