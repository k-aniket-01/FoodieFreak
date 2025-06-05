from django import forms
from django.core.exceptions import ValidationError

# Customer Registration Form
class CustomerRegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    contact = forms.CharField(max_length=15)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise ValidationError("Passwords do not match.")

# Canteen Owner Registration Form
class CanteenOwnerRegisterForm(forms.Form):
    owner_name = forms.CharField(max_length=100)
    canteen_name = forms.CharField(max_length=100)
    food_type = forms.ChoiceField(choices=[("veg", "Veg"), ("nonveg", "Non-Veg")])
    address = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password != confirm:
            raise ValidationError("Passwords do not match.")
