from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="InstituteDashboard"),
    path('department/create_read/', views.create_read_department, name="CreateReadDepartment"),
    path('designation/create_read', views.create_read_designation, name="CreateReadDesignation" ),
    path('staff/create_read', views.create_read_staff, name="CreateReadStaff" ),
    # TODO: add route for update and delete departments
    # TODO: add route for designation
    # TODO: add route for staff 
   
]