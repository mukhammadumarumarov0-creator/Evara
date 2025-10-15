from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from shop.forms import RegisterForm




def login_regester(request):
    if request.method == "POST":
        
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        
        
    return render(request,"shop/login-register.html",{"path":"Login"})


def logout_user(request):
    logout(request)
    return redirect('dashboard')


def create_account(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get("password")

            user=User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            return redirect('register')
        
        else:
            message={
                "path":'Register',
                "form":form
            }
            return render(request,"shop/register.html",context=message)
    
    form=RegisterForm()
    message={
                "path":'Register',
                "form":form
            }
    return render(request,"shop/register.html",context=message)
