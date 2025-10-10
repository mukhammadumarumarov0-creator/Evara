from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def dashboard(request):

    category=Category.objects.all()
    product=Product.objects.all()
    paginator=Paginator(product,4)

    page=request.GET.get('page')
    page_products=paginator.get_page(page)
    product_count=len(product)
    
    data={
        'path':"Mahsulotlar",
        "product":page_products,
        "product_count":product_count,
        'category':category,
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

    page=request.GET.get('page')
    page_products=paginator.get_page(page)

    data={
        'path':"Mahsulotlar",
        "product":page_products,
        'product_count':len(product)
        }
    
    return render(request,"shop/shop.html" ,context=data)


@login_required
def accounts(request):
    return render(request,"shop/accounts.html",context={'path':"Profilim"})

@login_required
def cart(request):
    return render(request,"shop/cart.html",context={'path':"Savatcha"})

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


def login_regester(request):
    if request.method == "POST":
        
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        
    return render(request,"shop/login-register.html")

def logout_user(request):
    logout(request)
    return redirect('dashboard')
            
def wish_list(request):
    return render(request,"shop/wishlist.html")

def create_account(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        print(first_name,last_name,email,password1,password2,username)

        if first_name and last_name and username and email and password1 and password2:
            user=User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            if password1==password2:
                user.set_password(password1)
                print(user)
                user.save()
                return redirect('register')
            else:
                print('password not match')

    return render(request,"shop/register.html")