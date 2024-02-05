from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.views import View
from .forms import UserForm, UserProfileForm

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
