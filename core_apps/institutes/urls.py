from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="InstituteDashboard"),
    path('department/create_read/', views.create_read_department, name="CreateReadDepartment"),
    path('designation/create_read/', views.create_read_designation, name="CreateReadDesignation" ),
    path('staff/create_read/', views.create_read_staff, name="CreateReadStaff" ),
    path('student/create_read/', views.create_read_student, name="CreateReadStudent" ),
    path('video_feed/<str:name>/', views.video_feed, name='video_feed'),
    path('academic/section/create_read/', views.create_read_academic_section, name="CreateReadAcademicSection" ),
    path('academic/class/create_read/', views.create_read_academic_class, name="CreateReadAcademicClass" ),
    path('academic/session/create_read/', views.create_read_academic_session, name="CreateReadAcademicSession" ),
    path('academic/Info/create_read/', views.create_read_academic_info, name="CreateReadAcademicInfo" ),
    path('academic/Info/delete/', views.delete_academic_info, name="DeleteAcademicInfo" ),
    
    # TODO: add route for update and delete departments
    # TODO: add route for designation
    # TODO: add route for staff 
    
   
]