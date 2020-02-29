from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts import models
from accounts.models import Customers,Products,Orders
from accounts.forms import OrderForm, ProductForm ,CustomerForm,CreateUserForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
@login_required(login_url='login')
@admin_only
def home(request):
    customer = Customers.objects.all
    product = Products.objects.all()
    order = Orders.objects.all()
    total_orders = len(order)
    pending = order.filter(status ='pending').count()
    delivered = order.filter(status = 'delivered').count()
    outfordelivery = order.filter(status = 'outfordelivery').count()
    context = {'customer':customer,'product':product,'order':order,
               'total_orders':total_orders,'pending':pending,
               'delivered':delivered,'outfordelivery':outfordelivery}
    return render(request,'crmaccounts/dashboard.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    product = Products.objects.all()


    context = {'product':product}
    return render(request, 'crmaccounts/products.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customers = Customers.objects.get(id=pk)
    order = customers.orders_set.all()
    total_orders = len(order)
    pending = order.filter(status='pending').count()
    delivered = order.filter(status='delivered').count()
    outfordelivery = order.filter(status='outfordelivery').count()
    context = {'order': order, 'customers': customers,
               'total_orders': total_orders, 'pending': pending,
               'delivered': delivered, 'outfordelivery': outfordelivery}
    return render(request,'crmaccounts/customer.html',context)

def orders(request,pk):
    pass
    return render(request, 'crmaccounts/orders.html')
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance = order)
    if request.method=="POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'crmaccounts/update_order.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Orders.objects.get(id=pk)
    order.delete()
    return redirect('/')
@login_required(login_url='login')
def add_product(request):
    if request.method=="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product')
    else:
        form = ProductForm()
        context = {'form':form}
        return render(request,'crmaccounts/add_product.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_product(request,pk):
    product = Products.objects.get(id=pk)
    if request.method=="POST":
        form = ProductForm(request.POST,instance=product,)
        if form.is_valid():
            form.save()
            return redirect('/product')
    else:
        form = ProductForm(instance=product)
        context = {'form':form}
        return render(request,'crmaccounts/update_product.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_product(request,pk):
    product = Products.objects.get(id=pk)
    product.delete()
    return redirect('/product')
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_order(request):
    if request.method =="POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm()
        context = {'form':form}
        return render(request,'crmaccounts/add_order.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_customer(request,pk):
    customer = Customers.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method=="POST":
        form = CustomerForm(request.POST     ,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        context = {'form':form}
        return render(request,'crmaccounts/update_customer.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request,pk):
    customer = Customers.objects.get(id=pk)
    customer.delete()
    return redirect('/')
@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    context = {'form':form}
    if request.method=="POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = request.POST.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customers.objects.create(
                user=user
            )
            messages.success(request, "Successfully Account is Created for" , +username)
            return redirect('login')
        else:
            return redirect('register')
    else:
        return render(request,'crmaccounts/registrationpage.html',context)
@unauthenticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,"Username or Password Worng")
    return render(request,'crmaccounts/loginpage.html')
def logoutpage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    customers = Customers.objects.get(user=request.user)
    order = request.user.customers.orders_set.all()
    total_orders = len(order)
    pending = order.filter(status='pending').count()
    delivered = order.filter(status='delivered').count()
    outfordelivery = order.filter(status='outfordelivery').count()
    context = {'order': order,'customers':customers,
               'total_orders': total_orders, 'pending': pending,
               'delivered': delivered, 'outfordelivery': outfordelivery}
    return render(request, 'crmaccounts/userpage.html', context)


def account_setting(request):
    customer=request.user.customers
    form = CustomerForm(instance=customer)
    if request.method=="POST":
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    return render(request,'crmaccounts/account_setting.html',{'form':form})