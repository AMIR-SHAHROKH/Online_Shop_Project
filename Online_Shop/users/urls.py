from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login-otp/', views.LoginWithPhoneOTPView.as_view(), name='log in with otp'),
    path('cart/', views.ShoppingCartView.as_view(), name='shopping_cart'),
]