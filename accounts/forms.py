from django import forms
from accounts.models import Products
from .models import Orders,Customers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
class ProductForm(forms.ModelForm):
    class Meta:
        model =Products
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model= Customers
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['first_name','last_name','email','username','password1','password2']