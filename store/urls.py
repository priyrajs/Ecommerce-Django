from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('updateItem/', views.updateItem, name="UpdateItem"),
    path('processOrder/', views.processOrder, name="processOrder"),

    path('login', views.userLogin, name="login"),
    path('register', views.userRegister, name="register"),
    path('logout', views.userLogout, name="logout"),
]