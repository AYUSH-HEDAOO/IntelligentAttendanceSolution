from django.urls import path

from IAS.core_apps.common import views

urlpatterns = [
<<<<<<< HEAD
    path('camera/', views.camera,name="Camera"),\
    path('mark_attendance/', views.mark_attendance,name="MarkAttendance"),
    path('attendance/add_photos/', views.add_images_to_dataset, name="AddImagesToDataset"),
    path('profile/update_read/', views.profile,name="ProfileUpdateRead"), 
=======
    path('mark_attendance/', views.mark_attendance, name="MarkAttendance"),
    path('attendance/add_photos/', views.add_images_to_dataset, name="AddImagesToDataset"),
    path('profile/update_read/', views.profile, name="ProfileUpdateRead"),
>>>>>>> develop
    path('attendance/read/', views.attendance_list, name="AttendanceList"),
    path("export/csv/", views.export_attendance_csv, name="ExportAttendanceCsv"),
    path("register_face/", views.register_face, name="register_face"),
    # path("export/pdf/", views.export_attendance_pdf, name="export_attendance_pdf"),
]
