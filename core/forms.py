from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

# ----------------------------
# 1. Customer Registration Form
# ----------------------------
class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set password properly (hash it)
        user.set_password(self.cleaned_data["password"])
        # Set role explicitly to customer
        user.role = 'customer'
        if commit:
            user.save()
        return user


# -------------------------------
# 2. Canteen Owner Registration Form
# -------------------------------
class CanteenOwnerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'canteen_name', 'address', 'contact', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Set role explicitly to owner
        user.role = 'owner'
        if commit:
            user.save()
        return user


# ----------------------------
# 3. Customer Login Form
# ----------------------------
class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)


# ----------------------------
# 4. Owner Login Form
# ----------------------------
class OwnerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)
