from django.shortcuts import render
from .models import Category,Product

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
    return render(request,"shop/login-register.html")

def wish_list(request):
    return render(request,"shop/wishlist.html")