from django.contrib import admin
from accounts.models import Customers,Products,Orders
class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','location','mobile']

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','description','category']

class AdminOrder(admin.ModelAdmin):
    list_display = ['customer','product','status']

admin.site.register(Customers,AdminCustomer)
admin.site.register(Products,AdminProduct)
admin.site.register(Orders,AdminOrder)