from django import forms
import re
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
   
   first_name=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'First Name'}),required=True)
   last_name=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'Last Name'}),required=True)
   username=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'Username'}),required=True)
   email=forms.EmailField(widget=forms.EmailInput(attrs={'class':"form__input",'placeholder':'Email'}),required=True)
   password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"form__input",'placeholder':'Password'}),required=True)
   reset_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"form__input",'placeholder':'Reset Password'}),required=True)
    
   
   def clean_first_name(self):
      value=self.cleaned_data['first_name']

      if value is None:
         raise forms.ValidationError("Ismni kiritish majburiy")
      
      if re.fullmatch(r"[A-Za-z]+", value) is None:
        raise forms.ValidationError("Ism faqat harflardan tashkil topishi kerak")
      return value
   

   def clean_last_name(self):
      value=self.cleaned_data['last_name']

      if value is None:
         raise forms.ValidationError("Familiyani kiritish majburiy")
      
      if re.fullmatch(r"['a-zA-z']+",value) is None:
         raise forms.ValidationError("Familiya faqat hariflardan tashkil topishi kerak")
      
      return value
   

   def clean_username(self):
      value=self.cleaned_data['username']

      if value is None:
         raise forms.ValidationError("usernmae kiritish majburiy")
      
      user=User.objects.filter(username=value)

      if user.exists():
         raise forms.ValidationError("bunday username alaqachon mavjud , iltimot boshqa kiriting")
      
      
      return value
   

   def clean_email(self):
      value=self.cleaned_data['email']

      if value is None:
         raise forms.ValidationError("email kiritish majburiy")
      
      email=User.objects.filter(email=value)

      if email.exists():
         raise forms.ValidationError("bunday email alaqachon mavjud , iltimot boshqa kiriting")
      
   
      return value


   def clean_reset_password(self):
         value=self.cleaned_data['reset_password']
         value2=self.cleaned_data['password']

         if value is None:
            raise forms.ValidationError("password kiritish majburiy")
         
         if value != value2:
            raise forms.ValidationError('Passwordlar bir xil bolishi kerak')
         
         
         

         return value
   

class ResetForm(forms.Form):
   first_name=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'First Name'}),required=True)
   last_name=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'Last Name'}),required=True)
   username=forms.CharField(widget=forms.TextInput(attrs={'class':"form__input",'placeholder':'Username'}),required=True)

   
  
   def clean_first_name(self):
      value=self.cleaned_data['first_name']

      if value is None:
         raise forms.ValidationError("Ismni kiritish majburiy")
      
      if re.fullmatch(r"[A-Za-z]+", value) is None:
        raise forms.ValidationError("Ism faqat harflardan tashkil topishi kerak")
      return value
   
   def clean_last_name(self):
      value=self.cleaned_data['last_name']

      if value is None:
         raise forms.ValidationError("Familiyani kiritish majburiy")
      
      if re.fullmatch(r"['a-zA-z']+",value) is None:
         raise forms.ValidationError("Familiya faqat hariflardan tashkil topishi kerak")
      
      return value
   
   def clean_username(self):
      value=self.cleaned_data['username']

      if value is None:
         raise forms.ValidationError("usernmae kiritish majburiy")
      
      user=User.objects.filter(username=value)

      if user.exists():
         raise forms.ValidationError("bunday username alaqachon mavjud , iltimot boshqa kiriting")
      
      
      return value
   





import re
from django import forms

class ResetPasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'Current password'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'New password'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form__input', 'placeholder': 'Confirm new password'
    }))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # <<== bu juda muhim
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        c_password = cleaned_data.get('current_password')
        n_password = cleaned_data.get('new_password')
        n_password2 = cleaned_data.get('new_password2')

        # 1️⃣ user kelganini tekshirish
        if not self.user:
            raise forms.ValidationError("Foydalanuvchi aniqlanmadi.")

        # 2️⃣ Joriy parolni tekshirish
        if not self.user.check_password(c_password):
            raise forms.ValidationError("Joriy parol noto‘g‘ri.")

        # 3️⃣ Parollarni solishtirish
        if n_password != n_password2:
            raise forms.ValidationError("Yangi parollar bir xil bo‘lishi kerak.")

        # 4️⃣ Eski bilan yangi parol bir xil emasligini tekshirish
        if c_password == n_password:
            raise forms.ValidationError("Yangi parol joriy parol bilan bir xil bo‘lishi mumkin emas.")

        # 5️⃣ Eng oddiy validatsiya (kamida 8 ta belgi)
        if len(n_password) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo‘lishi kerak.")

        return cleaned_data

