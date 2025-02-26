from django.urls import path
from . import views

urlpatterns = [
    path('mark_attendance/', views.mark_attendance,name="MarkAttendance"),
    path('attendance/add_photos/', views.add_images_to_dataset, name="AddImagesToDataset"),
    path('profile/update_read/', views.profile,name="ProfileUpdateRead"), 
]