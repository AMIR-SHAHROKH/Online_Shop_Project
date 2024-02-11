from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.views import View
import random
from django.contrib import messages
from .forms import LoginForm
import string
from .forms import EmailForm, OTPForm , AddressForm 
from django.views.generic import TemplateView

class AccountView(TemplateView):
    template_name = 'users/account.html'
class ShoppingCartView(View):
    def get(self, request):
        return render(request, 'users/cart.html')
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
        # Your logic to fetch shopping cart items and process data
        # For example, fetching items from the shopping cart model
        # Replace 'ShoppingCartItem' with your actual model name
        # cart_items = ShoppingCartItem.objects.all()
    #     cart_items = []  # Placeholder for cart items
    #     context['cart_items'] = cart_items
    #     return context    
# template_name = 'users/shopping_cart.html'

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to your desired URL after successful login
            else:
                # Authentication failed, display error message
                error_message = 'Invalid username/email or password.'
                messages.error(request, error_message)
                return render(request, 'users/login.html', {'form': form, 'error_message': error_message})
        else:
            # Form is invalid, redisplay the login form with errors
            return render(request, 'users/signup.html', {'form': form})



class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('login')  # Redirect to the login page after logout

class SignUpView(View):
    def get(self, request):
        user_form = UserForm()
        address_form = AddressForm()
        return render(request, 'users/signup.html', {'user_form': user_form, 'address_form': address_form})
    
    def post(self, request):
        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save()  # Save the user form
            address = address_form.save(commit=False)
            address.user = user  # Assign the User instance, not the form data
            address.save()
            # Assuming auth_login function is defined elsewhere
            auth_login(request, user)
            return redirect('/')  # Redirect to your desired URL after successful signup
        else:
            # Add an error message to be displayed in the template
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'users/signup.html', {'user_form': user_form, 'address_form': address_form})
        
class LoginWithEmailOTPView(View):
    def get(self, request):
        return render(request, 'users/login_with_email_otp.html')

    def post(self, request):
        if 'email' in request.POST:  # Check if email form is submitted
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                otp = self.generate_otp()
                user.otp = otp
                user.otp_created_at = timezone.now()
                user.save()
                self.send_otp_email(email, otp)
                request.session['email'] = email  # Store email in session
                return render(request, 'users/login_with_email_otp.html', message = "we sent you the email")
            except User.DoesNotExist:
                error = 'No user with this email address found.'
                return render(request, 'users/login_with_email_otp.html', {'error': error})
        elif 'otp' in request.POST:  # Check if OTP form is submitted
            email = request.session.get('email')
            otp = request.POST.get('otp')
            try:
                user = User.objects.get(email=email)
                if user.otp == otp and user.otp_created_at > timezone.now() - timezone.timedelta(minutes=5):
                    # OTP verification successful, proceed with login
                    del request.session['email']  # Remove email from session
                    # Add your login logic here, for example:
                    # login(request, user)
                    return redirect('home')  # Redirect to home page after login
                else:
                    error = 'Invalid OTP or OTP expired.'
                    return render(request, 'users/login_with_email_otp.html', {'error': error})
            except User.DoesNotExist:
                error = 'No user with this email address found.'
                return render(request, 'users/login_with_email_otp.html', {'error': error})
        return render(request, 'users/login_with_email_otp.html')  # Default rendering

    def generate_otp(self, length=6):
        characters = string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def send_otp_email(self, email, otp):
        subject = 'Your One-Time Password (OTP)'
        message = f'Your OTP is: {otp}'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email])