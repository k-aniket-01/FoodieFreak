from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from .forms import (
    CustomerRegistrationForm,
    CanteenOwnerRegisterForm,
    CustomerLoginForm,
    OwnerLoginForm
)

User = get_user_model()

# Public pages
def home(request):
    return render(request, 'home.html')

def canteen_owner(request):
    return render(request, 'canteen_owner.html')

def contactus(request):
    return render(request, 'contactus.html')

def customer(request):
    return render(request, 'customer.html')


# Registration Views
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login_customer')
        else:
            messages.error(request, 'Registration failed. Please fix the errors below.')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})


def register_canteen_owner(request):
    if request.method == 'POST':
        form = CanteenOwnerRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['owner_name'],
                password=form.cleaned_data['password'],
                role='owner'
            )
            user.canteen_name = form.cleaned_data['canteen_name']
            user.contact = form.cleaned_data['contact']
            user.address = form.cleaned_data['address']
            user.save()
            messages.success(request, "Canteen Owner registered successfully.")
            return redirect('login_owner')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CanteenOwnerRegisterForm()
    return render(request, 'register_canteen_owner.html', {'form': form})


# Login Views
def login_customer(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'customer':
                login(request, user)
                return redirect('customer_dashboard')
            else:
                messages.error(request, "Invalid credentials or not a customer.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = CustomerLoginForm()
    return render(request, 'login_customer.html', {'form': form})


def login_owner(request):
    if request.method == 'POST':
        form = OwnerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'owner':
                login(request, user)
                return redirect('owner_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an owner.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = OwnerLoginForm()
    return render(request, 'login_owner.html', {'form': form})


# Dashboards
@login_required
def customer_dashboard(request):
    return render(request, 'customer_dashboard.html')

@login_required
def owner_dashboard(request):
    return render(request, 'owner_dashboard.html')


# Optional: Unified Login View (if you still want one)
def login_common(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'owner':
                return redirect('owner_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login_common.html', {'form': form})
