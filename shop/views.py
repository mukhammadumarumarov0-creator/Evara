from django.shortcuts import render

def dashboard(request):
    return render(request,"shop/index.html")

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