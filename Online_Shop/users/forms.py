from django import forms
from django.contrib.auth.models import User
from .models import UserProfile , Address
from django.contrib.auth.forms import AuthenticationForm

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'address']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    
class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)
    email = forms.EmailField(widget=forms.HiddenInput())