from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="InstituteDashboard"),
    path('department/create_read/', views.create_read_department, name="CreateReadDepartment"),
    path('designation/create_read', views.create_read_designation, name="CreateReadDesignation" ),
    path('staff/create_read', views.create_read_staff, name="CreateReadStaff" ),
    path('student/create_read', views.create_read_student, name="CreateReadStudent" ),
    path('student/create_read', views.create_read_academicSection, name="CreateReadAcademicSection" ),
    path('student/create_read', views.create_read_academicClass, name="CreateReadAcademicClass" ),
    
    # TODO: add route for update and delete departments
    # TODO: add route for designation
    # TODO: add route for staff 
    
   
]