from django.shortcuts import render,redirect
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def dashboard(request):

    category=Category.objects.all()
    product=Product.objects.all()

    categories={"category":category,"product":product}

    return render(request,"shop/index.html" ,categories)

@login_required
def details(request,id):

    product=Product.objects.get(id=id)


    return render(request,"shop/details.html",context={'product':product})

@login_required
def shop(request):
    product=Product.objects.all()
    for i in product:
        print(i.discount_price)

    
    return render(request,"shop/shop.html" ,context={'path':"Mahsulotlar","product":product})


@login_required
def accounts(request):
    return render(request,"shop/accounts.html",context={'path':"Profilim"})

@login_required
def cart(request):
    return render(request,"shop/cart.html",context={'path':"Savatcha"})

@login_required
def check_out(request):
    return render(request,"shop/checkout.html")



def login_regester(request):
    if request.method == "POST":
        
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        print(user)

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