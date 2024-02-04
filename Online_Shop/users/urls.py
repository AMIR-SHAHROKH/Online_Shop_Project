from django.urls import path
from . import views
from .views import signup

urlpatterns = [
    # path('profile/', views.profile_view, name='profile'),
    path('signup/', signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]