from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="StudentDashboard"),
    path('attendance/create_read/', views.attendance_create_read, name="StudentAttendanceCreateRead"),
]