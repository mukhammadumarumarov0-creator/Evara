from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from shop.forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


class LoginUserView(View):
    def get(self, request):
        return render(request, "shop/login-register.html", context={"path": "Login"})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(
                request,
                "shop/login-register.html",
                context={
                    "path": "Login",
                    "error": "Username yoki parol noto‘g‘ri!"
                }
            )

class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('dashboard')

class CreatAccountView(View):
 def get(self,request):

    form=RegisterForm()
    message={
                "path":'Register',
                "form":form
            }
    return render(request,"shop/register.html",context=message)
 
 def post(self,request):
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
    

