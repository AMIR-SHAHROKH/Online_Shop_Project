from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserForm
from django.utils import timezone
from django.views import View
import random
from django.contrib import messages
from .forms import LoginForm
import string
from .backend import custom_authenticate
from .forms import EmailForm, OTPForm , AddressForm 
from django.views.generic import TemplateView
from melipayamak import Api
from django.contrib.auth import get_user_model
from users.models import User
from django.http import JsonResponse

# Get the custom User model


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


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = custom_authenticate(request, username=username, password=password)
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
            return render(request, 'users/login.html', {'form': form})
        
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

class LoginWithPhoneOTPView(View):
    template_name = 'users/otp_login.html'

    def get(self, request):
        return render(request, self.template_name)

    def generate_otp(self):
            """
            Generates a 6-digit OTP.
            """
            return ''.join(random.choices('0123456789', k=6))
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        
        # Check if the phone number exists in the Users
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this phone number does not exist'}, status=400)

        # Send SMS with OTP using your API
        api = Api(user.username, user.password)  # provide your credentials here
        sms = api.sms()
        to = phone_number
        _from = '50002710055405'
        otp = self.generate_otp()  # you need to implement the OTP generation function
        text = f'Your OTP is: {otp}'
        # Send OTP message
        response = sms.send(to, _from,text)
        print(text)
        print(response)
        # Store the OTP in session for verification later
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number
        request.session.save()

        return JsonResponse({'success': 'OTP sent successfully'}, status=200)

class VerifyOTPAndLoginView(View):
    def post(self, request, *args, **kwargs):
        otp_entered = request.POST.get('otp')
        phone_number = request.POST.get('phone_number')

        # Retrieve the OTP from session
        otp_stored = request.session.get('otp')
        
        if otp_entered == otp_stored:
            # If OTP is correct, authenticate the user and log in
            user = User.objects.get(profile__phone_number=phone_number)
            if user:
                user = authenticate(request, username=user.username, password=user.password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': 'User logged in successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Authentication failed'}, status=400)
            else:
                return JsonResponse({'error': 'User does not exist'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

# class LoginWithPhoneOTPView(View):
#     template_name = 'users/otp_login.html'

#     def get(self, request):
#         return render(request, self.template_name)

#     def generate_otp(self):
#         # Implement your OTP generation logic here
#         return '123456'  # Replace with your OTP generation logic

#     def send_otp_sms(self, phone_number, otp):
#         # Initialize the API with your credentials
#         username = 'your_username'
#         password = 'your_password'
#         api = Api(username, password)
        
#         # Prepare the SMS message
#         to = phone_number
#         _from = 'your_sender_number'
#         text = f'Your OTP is: {otp}'
        
#         # Send the OTP SMS
#         response = api.sms().send(to, _from, text)
        
#         if response['result'] != '1':
#             # Failed to send OTP SMS
#             messages.error(request, 'Failed to send OTP SMS.')

#     def post(self, request):
#         if 'phone_number_form' in request.POST:
#             phone_number = request.POST.get('phone_number')
#             try:
#                 user = User.objects.get(phone_number=phone_number)
#                 otp = self.generate_otp()
#                 user.otp = otp
#                 user.otp_created_at = timezone.now()
#                 user.save()
#                 self.send_otp_sms(phone_number, otp)
#                 request.session['phone_number'] = phone_number
#                 messages.success(request, 'OTP sent successfully!')
#                 return render(request, self.template_name, {'otp_sent': True})
#             except User.DoesNotExist:
#                 messages.error(request, 'No user with this phone number found.')
#                 return render(request, self.template_name)

#         elif 'otp_form' in request.POST:
#             phone_number = request.session.get('phone_number')
#             otp = request.POST.get('otp')
#             try:
#                 user = User.objects.get(phone_number=phone_number)
#                 if user.otp == otp and user.otp_created_at > timezone.now() - timezone.timedelta(minutes=5):
#                     del request.session['phone_number']
#                     login(request, user)
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'Invalid OTP or OTP expired.')
#                     return render(request, self.template_name, {'otp_sent': True})
#             except User.DoesNotExist:
#                 messages.error(request, 'No user with this phone number found.')
#                 return render(request, self.template_name)
