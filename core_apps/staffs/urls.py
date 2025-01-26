from django.urls import path
from . import views
from core_apps.institutes import views as institutes_views

urlpatterns = [
    path('dashboard/', views.dashboard,name="StaffDashboard"),
    path('profile/update_read/', views.profile,name="StaffProfileUpdateRead"),
    path('student/create_read/',institutes_views.create_read_student, name="StaffCreateReadStudent")
    
]