from django.urls import path
from . import views

urlpatterns = [
    path('', views.login,name="Login"),
    path('logout/', views.user_logout,name="Logout"),
    path('register/', views.register,name="Register"),
    
]