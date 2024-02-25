from django import forms
from .models import UserProfile , Address , User
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','phone_number']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'address']

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    
class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)
    phone_number = forms.CharField(label='phone number')
class CheckOTP(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)