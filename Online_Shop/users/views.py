from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserForm, UserProfileForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views import View
import random
import string
from .forms import EmailForm, OTPForm
class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            # Return an error message or handle invalid login credentials
            return render(request, 'accounts/login.html', {'error_message': 'Invalid username or password'})

class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')  # Redirect to the login page after logout

class SignUpView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'accounts/signup.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page after successful signup
        else:
            return render(request, 'accounts/signup.html', {'user_form': user_form, 'profile_form': profile_form})

class LoginWithEmailOTPView(View):
    def get(self, request):
        email_form = EmailForm()
        otp_form = OTPForm()
        return render(request, 'login_with_email_otp.html', {'email_form': email_form, 'otp_form': otp_form})

    def post(self, request):
        if 'email_form' in request.POST:  # Check if email form is submitted
            email_form = EmailForm(request.POST)
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    otp = self.generate_otp()
                    user.profile.otp = otp
                    user.profile.otp_created_at = timezone.now()
                    user.profile.save()
                    self.send_otp_email(email, otp)
                    return redirect('otp_verification')
                except User.DoesNotExist:
                    error = 'No user with this email address found.'
                    return render(request, 'login_with_email_otp.html', {'email_form': email_form, 'otp_form': OTPForm(), 'error': error})
        elif 'otp_form' in request.POST:  # Check if OTP form is submitted
            otp_form = OTPForm(request.POST)
            if otp_form.is_valid():
                email = otp_form.cleaned_data['email']
                otp = otp_form.cleaned_data['otp']
                try:
                    user = User.objects.get(email=email)
                    if user.profile.otp == otp and user.profile.otp_created_at > timezone.now() - timezone.timedelta(minutes=5):
                        login(request, user)
                        return redirect('home')
                    else:
                        error = 'Invalid OTP or OTP expired.'
                        return render(request, 'login_with_email_otp.html', {'email_form': EmailForm(), 'otp_form': otp_form, 'error': error})
                except User.DoesNotExist:
                    error = 'No user with this email address found.'
                    return render(request, 'login_with_email_otp.html', {'email_form': EmailForm(), 'otp_form': otp_form, 'error': error})
        return render(request, 'login_with_email_otp.html', {'email_form': EmailForm(), 'otp_form': OTPForm()})  # Default rendering

    def generate_otp(self, length=6):
        characters = string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def send_otp_email(self, email, otp):
        subject = 'Your One-Time Password (OTP)'
        message = f'Your OTP is: {otp}'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email])