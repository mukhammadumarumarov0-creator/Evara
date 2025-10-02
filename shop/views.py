from django.shortcuts import render,redirect
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

def dashboard(request):

    category=Category.objects.all()
    product=Product.objects.all()

    for p in product:
        if p.discount>0:
            p.discount=p.price-(p.price*p.discount/100)

    categories={"category":category,"product":product}

    return render(request,"shop/index.html" ,categories)


def details(request):
    return render(request,"shop/details.html")

def shop(request):
    return render(request,"shop/shop.html")

def accounts(request):
    return render(request,"shop/accounts.html")

def cart(request):
    return render(request,"shop/cart.html")

def check_out(request):
    return render(request,"shop/checkout.html")

def compare(request):
    return render(request,"shop/compare.html")

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