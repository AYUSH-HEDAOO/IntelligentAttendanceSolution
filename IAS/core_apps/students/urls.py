from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="StudentDashboard"),
    path('profile/update_read/', views.profile,name="StudentProfileUpdateRead"),
    path('attendance/create_read/', views.attendance_create_read, name="StudentAttendanceCreateRead"),
    path('attendance/add_photos/', views.add_photos, name="StudentAttendanceAddPhotos"),
]