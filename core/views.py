from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def canteen_owner(request):
    return render(request, 'canteen_owner.html' )

def contactus(request):
    return render(request, 'contactus.html' )

def customer(request):
    return render(request, 'customer.html' )

from django.shortcuts import render, redirect
from .forms import CustomerRegisterForm, CanteenOwnerRegisterForm
from django.contrib import messages

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            # Save logic here
            messages.success(request, "Customer registered successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomerRegisterForm()
    return render(request, 'register_customer.html', {'form': form})

def register_canteen_owner(request):
    if request.method == 'POST':
        form = CanteenOwnerRegisterForm(request.POST)
        if form.is_valid():
            # Save logic here
            messages.success(request, "Canteen Owner registered successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CanteenOwnerRegisterForm()
    return render(request, 'register_canteen_owner.html', {'form': form})
