from store.utils import cartData, cookieCart
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.contrib.auth.models import User
from django.core.signals import request_finished

from django.dispatch import receiver
from django.db.models.signals import post_save
from store.apis import *
from time import sleep

# Create your views here.
def store(requests):
    
    data = cartData(requests)  
    cartItems = data['cartItems']

    # test1 = User.objects.get(last_name="user")
    # print(test1.first_name)
    # test2 = User.objects.filter(last_name="user")
    # print(test2.first_name)

    courses = Course.objects.all()
    context = {
        "courses" : courses,'cartItems':cartItems }
    return render(requests,'store.html',context)

def cart(requests):
    
    data = cartData(requests)  
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    context = {"items" : items, 'order' : order,'cartItems':cartItems}

    return render(requests,'cart.html',context)

def checkout(requests):

    data = cartData(requests)  
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    context = {"items" : items, 'order' : order,'cartItems':cartItems}

    context = {"items" : items, 'order' : order,'cartItems':cartItems}
    
    return render(requests,'checkout.html',context)
    
def updateItem(request):
    courseid = request.POST.get('courseid')
    action = request.POST.get('action')

    customer = request.user.customer
    print(f"Id:{courseid}, action:{action},user:{customer}")
    course = Course.objects.get(id=courseid)
    order, created = Order.objects.get_or_create(customer=customer,complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,course=course)

    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    else:
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Added",safe=False)

def processOrder(request):
    total = float(request.POST.get('total'))
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete = False)
    else:
        fname = request.POST.get('fname').strip()
        lname = request.POST.get('lname').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        cookieData = cookieCart(request)
        items = cookieData['items']
        
        user = User.objects.create_user(username=email,email=email,password=password,first_name=fname,last_name=lname)
        # user.first_name = fname
        # user.last_name = lname
        # user.save()
        name = fname+" "+lname
        customer = Customer.objects.create(user=user,name=name, email=email)
        order = Order.objects.create(customer=customer,complete=False)

        for item in items:
            course = Course.objects.get(id=item['course']['id'])
            orderItem = OrderItem.objects.create(order=order,course=course)

    if total == order.get_cart_total:
        order.complete = True
    order.transaction_id = transaction_id
    order.save()
    mdl_create_user(customer,course,True)
    return JsonResponse("Order Placed",safe=False)

def userLogin(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,"login.html")
    return render(request,"login.html")

def userRegister(request):
    if request.method =="POST":
        fname = request.POST.get("fname").strip()
        lname = request.POST.get("lname").strip()
        email = request.POST.get("email").strip()
        phone = request.POST.get("phone").strip()
        password  = request.POST.get("password").strip()
        user = User.objects.create_user(username=email,email=email,password=password,first_name=fname,last_name=lname)
        # user.first_name = fname
        # user.last_name = lname
        # user.phone = phone
        # user.save()
        name = fname+" "+lname
        customer = Customer.objects.create(user=user,name=name, email=email)
        mdl_create_user(customer,"",False)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,"login.html")
    return render(request,"register.html")

def userLogout(request):
    logout(request)
    return redirect("/login")

# @receiver(post_save, sender=Customer)
# def user_saved(sender,instance,**kwargs):
#     #mdl_create_user(instance)
#     print(instance)
#     print(dispatch_uid)

# @receiver(post_save, sender=Order)
# def user_saved(sender,instance,**kwargs):
#     if(instance.complete):
#         mdl_enrol_user(instance)
    