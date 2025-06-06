from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),
    path('contact/', views.contactus, name='contactus'),
    path('owner/',views.canteen_owner, name='owner'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/owner/', views.register_canteen_owner, name='register_owner'),

    path('login/customer/', views.login_customer, name='login_customer'),
    path('login/owner/', views.login_owner, name='login_owner'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),


]
