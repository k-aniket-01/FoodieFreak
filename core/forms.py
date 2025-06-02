from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('customer', 'Customer'), ('owner', 'Canteen Owner')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']



# core/forms.py
from django import forms
from .models import FoodItem

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'available']
