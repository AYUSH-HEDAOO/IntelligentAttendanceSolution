from django import forms
from .models import Department,Designation, Institute
from core_apps.staffs.models import Staff
from django.db import transaction
from django.contrib.auth import get_user_model
from core_apps.users.models import Role
from django.contrib.auth.hashers import make_password
from core_apps.common.models import RoleType

AUTH_USER = get_user_model()


class DepartmentForm(forms.Form):
    department_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'department_name'})
    )
    
    
    def save(self, institute):
        department_name = self.cleaned_data['department_name']
        department = Department.is_department_exists(department_name, institute)

        if department:
            return False, "Department already exists!"

        try:
            
            Department.objects.create(
                department_name=department_name,
                institute=institute
            )

            return True, "Department created successfully"
        
        except Exception as e:
            return False, f"An error occurred: {e}"
        
   
class DesignationForm(forms.Form):
    designation_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'designation_name'})
    )
    
    
    def save(self, institute):
        designation_name = self.cleaned_data['designation_name']
        designation = Designation.is_designation_exists(designation_name, institute)

        if designation:
            return False, "Designation already exists!"

        try:
            
            Designation.objects.create(
                designation_name=designation_name,
                institute=institute
            )

            return True, "Designation created successfully"
        
        except Exception as e:
            return False, f"An error occurred: {e}"
        

class StaffForm(forms.Form):
    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'})
    )
    last_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'})
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email'})
    )
    password = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'password'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'department'}),
        empty_label="Select Department"
    )
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'designation'}),
        empty_label="Select Designation"
    )
    
    def save(self, institute):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        department = self.cleaned_data['department']
        designation = self.cleaned_data['designation']

        try:
            with transaction.atomic():

                # Create the User
                user = AUTH_USER.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=make_password(password),
                )
                # Create the Role
                role = Role.objects.create(
                    user=user,
                    institute=institute,
                    role_type=RoleType.STAFF
                )
                
                # Create the Staff
                Staff.objects.create(
                    role=role,
                    department=department,
                    designation=designation,
                    institute=institute
                )
                
            return True, "staff created successfully"
        
        except Exception as e:
            return False, f"An error occurred: {e}"
        