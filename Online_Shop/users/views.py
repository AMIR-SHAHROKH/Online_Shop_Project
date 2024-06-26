from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserForm
from django.http import Http404
from django.views import View
import random
from django.contrib import messages
from .forms import LoginForm
from django.urls import reverse
from .backend import custom_authenticate
from .forms import EmailForm, OTPForm , AddressForm , CheckOTP
from django.views.generic import TemplateView
from melipayamak import Api
from django.contrib.auth import get_user_model
from users.models import User,Address
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from users.models import User  # Import the custom user model
from orders.serializers import OrderSerializer
from orders.models import Order
from django.conf import settings
import redis
from django.contrib.auth import authenticate, logout , login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,AddressSerializer
from users.tasks import send_email_task
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics

# Get the custom User model

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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
            user = custom_authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                subject = 'Welcome to Our Website!'
                message = 'Thank you for signing up. We hope you enjoy using our website.'
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                # response = send_mail(subject, message, from_email, to_email)
                # print(response)
                send_email_task.delay(subject, message, from_email, to_email)
                return redirect(reverse('products:logged_in_main_page'))   # Redirect to your desired URL after successful login
            else:
                # Authentication failed, display error message
                error_message = 'Invalid username or password.'
                messages.error(request, error_message)
                return render(request, 'users/login.html', {'form': form, 'error_message': error_message})
        else:
            # Form is invalid, redisplay the login form with errors
            return render(request, 'users/login.html', {'form': form})
        
class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('products:main_page')  # Redirect to the login page after logout

class SignUpView(View):
    def get(self, request):
        user_form = UserForm()
        address_form = AddressForm()
        return render(request, 'users/signup.html', {'user_form': user_form, 'address_form': address_form})
    
    def post(self, request):

        password = request.POST.get('password')

        user_form = UserForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save()  # Save the user form
            user.password = make_password(password)
            user.save()
            address = address_form.save(commit=False)
            address.user = user  # Assign the User instance, not the form data
            address.save()
            # Assuming auth_lo
            # gin function is defined elsewhere
            auth_login(request, user)
            subject = 'Welcome to Our Website!'
            message = 'Thank you for signing up. We hope you enjoy using our website.'
            from_email = settings.EMAIL_HOST_USER
            to_email = [user_form.cleaned_data['email']]
            # send_mail(subject, message, from_email, to_email)
            send_email_task.delay(subject, message, from_email, to_email)
            return redirect(reverse('products:logged_in_main_page'))  # Redirect to your desired URL after successful signup
        else:
            # Add an error message to be displayed in the template
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'users/signup.html', {'user_form': user_form, 'address_form': address_form})
        
class LoginWithPhoneOTPView(View):
    template_name = 'users/otp_login.html'

    def get(self, request):
        form = OTPForm()
        return render(request, self.template_name,{'form': form})

    def generate_otp(self):
            """
            Generates a 6-digit OTP.
            """
            return ''.join(random.choices('0123456789', k=6))
    def post(self, request):
        form = OTPForm(request.POST)
        phone_number = request.POST.get('phone_number')
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
        # Check if the phone number exists in the Users
        try:
            user = User.objects.get(phone_number=phone_number)
            print(user)
        except User.DoesNotExist:
            messages.error(request, 'User with this phone number does not exist')
            return render(request, self.template_name)


        # Send SMS with OTP using your API
        user.password = "8e7deb21-3bc9-4810-8818-addf28bdde1c"
        user.username = "09124555406"
        api = Api(user.username, user.password)  # provide your credentials here
        sms = api.sms()
        to = phone_number
        _from = '50002710055405'
        otp = self.generate_otp()  # you need to implement the OTP generation function
        text = f'Your OTP is: {otp}'
        redis_client.setex(to,120, otp)
        # Send OTP message
        response = sms.send(to, _from,text)
        print(text)
        print(response)
        # Store the OTP in session for verification later
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number
        request.session.save()

        messages.success(request, 'OTP sent successfully')
        return redirect(reverse('users:enter-otp'))

class VerifyOTPAndLoginView(View):
    template_name = 'users/otp_enter.html'

    def get(self, request):
        form = CheckOTP(request.POST) 
        return render(request, self.template_name,{'form': form })
    
    def post(self, request, *args, **kwargs):
        form = CheckOTP(request.POST)  # Instantiate the OTPForm with POST data
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            url_path = reverse("users:enter-otp")
            phone_number = request.session["phone_number"]
            # Retrieve the OTP from session
            otp_stored = request.session.get('otp')

            if redis_client.get(phone_number).decode("utf-8") == otp_entered:
                # If OTP is correct, authenticate the user and log in
                try:
                    print(phone_number)
                    user = User.objects.get(phone_number= phone_number)
                    print(user)
                    if user is not None:
                        print("user.username")
                        print("hello")
                        login(request, user)
                        messages.success(request, 'User logged in successfully')
                        return redirect(reverse('products:logged_in_main_page'))
                    else:
                        messages.error(request, 'User does not exist')
                except User.DoesNotExist:
                    messages.error(request, 'User does not exist')
            else:
                messages.error(request, 'Invalid OTP')
        else:
            # If form is invalid, handle the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

        # If the form is not valid or authentication fails, return to the same page
        return render(request, 'users/otp_enter.html', {'form': form })
    
class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve orders for the current user
        orders = Order.objects.filter(user=self.request.user)
        # Serialize orders
        order_serializer = OrderSerializer(orders, many=True)
        context['orders'] = order_serializer.data
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Check if the current user is the same as the requested user
        if obj != self.request.user:
            raise Http404("You are not authorized to view this page")
        return obj
class OrdersView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/orders.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve orders for the current user
        orders = Order.objects.filter(user=self.request.user)
        # Serialize orders
        order_serializer = OrderSerializer(orders, many=True)
        context['orders'] = order_serializer.data
        return context
class AddressView(View):
    def get(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve addresses related to the currently logged-in user
            user_addresses = Address.objects.filter(user=request.user)
        else:
            # If the user is not authenticated, set user_addresses to None
            user_addresses = None
        print(user_addresses)
        return render(request, 'users/address.html', {'user_addresses': user_addresses})

class ShippingAddressCheckView(APIView):
    def get(self, request):
        # Retrieve the user's shipping address
        shipping_address = Address.objects.filter(user=request.user, is_shipping_address=True).first()

        if shipping_address:
            # Serialize the shipping address
            serializer = AddressSerializer(shipping_address)
            return Response(serializer.data)
        else:
            # Return an empty response if there is no shipping address
            return Response({})
        
class ShippingAddressView(APIView):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def put(self, request):
        address_id = request.data.get('address_id')
        try:
            address = Address.objects.get(user=request.user, address_id=address_id)
            # Set the selected address as the shipping address
            Address.objects.filter(user=request.user).update(is_shipping_address=False)
            address.is_shipping_address = True
            address.save()
            return Response(status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class UserInfoAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        addresses = AddressSerializer(user.addresses.all(), many=True).data
        return render(request, 'user_detail.html', {'user': user, 'addresses': addresses})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Process new address data and create a new address
            new_address_data = request.data.get('new_address', {})
            new_address_serializer = AddressSerializer(data=new_address_data)
            if new_address_serializer.is_valid():
                new_address_serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(new_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        addresses = user.addresses.all()
        context = {
            'user': user,
            'addresses': addresses
        }
        return render(request, 'users/user_info_update.html', context)

    def post(self, request):
        user = request.user
        # Process the form data
        email = request.POST.get('email')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        # Check if the new phone number is unique
        if User.objects.exclude(id=user.id).filter(phone_number=phone_number).exists():
            return JsonResponse({'status': 'error', 'message': 'Phone number is not unique.'}, status=400)

        # Update user information
        user.email = email
        user.username = username
        user.phone_number = phone_number
        user.save()

        # Update or create addresses for the current user
        new_street = request.POST.get('new_street')
        new_city = request.POST.get('new_city')
        new_state = request.POST.get('new_state')
        new_postal_code = request.POST.get('new_postal_code')
        new_country = request.POST.get('new_country')

        # Create a new address associated with the current user
        new_address = Address.objects.create(
            user=user,
            street=new_street,
            city=new_city,
            state=new_state,
            postal_code=new_postal_code,
            country=new_country
        )

        return JsonResponse({'status': 'success', 'message': 'User information updated successfully!'})