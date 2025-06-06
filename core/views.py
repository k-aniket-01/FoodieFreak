from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from datetime import datetime 
import random

def current_year(request):
    return {'current_year': datetime.now().year}

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Update the role in the associated Profile created by the signal
            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            role = user.profile.role  # get user's role
            if role == 'owner':
                return redirect('owner_dashboard')
            elif role == 'customer':
                return redirect('customer_dashboard')
            else:
                return redirect('home')  # fallback redirect
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def customer_dashboard(request):
    if request.user.profile.role != 'customer':
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'customer_dashboard.html')


@login_required
def owner_dashboard(request):
    if request.user.profile.role != 'owner':
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'owner_dashboard.html')


from .models import FoodItem
from django.contrib.auth.decorators import login_required

@login_required
def food_item_list(request):
    if request.user.profile.role != 'owner':
        return redirect('home')
    items = FoodItem.objects.filter(owner=request.user)
    return render(request, 'owner/food_item_list.html', {'items': items})


# core/views.py
from .forms import FoodItemForm

@login_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.owner = request.user
            food_item.save()
            return redirect('food_item_list')
    else:
        form = FoodItemForm()
    return render(request, 'add_food_item.html', {'form': form})






