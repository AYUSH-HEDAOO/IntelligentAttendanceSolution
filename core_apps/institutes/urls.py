from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name="InstituteDashboard"),
    path('department/create_read/', views.create_read_department, name="CreateReadDepartment")
    # TODO: add route for update and delete departments
    # TODO: add route for designation
    # TODO: add route for staff 
   
]