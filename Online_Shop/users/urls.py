from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login-otp/', views.LoginWithPhoneOTPView.as_view(), name='log in with otp'),
    path('otp-enter/', views.VerifyOTPAndLoginView.as_view(), name='enter-otp'),
    path('<str:username>', views.UserProfileView.as_view(), name='profile'),
    path('cart/', views.ShoppingCartView.as_view(), name='shopping_cart'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api/user-info/', views.UserInfoAPIView.as_view(), name='user-info-api'),
    path('user-info/', views.UserInfoView.as_view(), name='user-info'),
    path('addresses/', views.AddressView.as_view(), name='addresses'),
    path('orders/<str:username>', views.OrdersView.as_view(), name='user-orders'),
    path('api/addresses/', views.ShippingAddressView.as_view(), name='addresses-api'),
    path('api/address-check/', views.ShippingAddressCheckView.as_view(), name='addresses-check-api'),
]