from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('customer/', views.customer, name='customer'),
    path('contact/', views.contactus, name='contactus'),
    path('owner/',views.canteen_owner, name='owner'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/owner/', views.register_canteen_owner, name='register_owner'),

]
