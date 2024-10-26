from django import forms
from .models import Department
from django.db import models, transaction

class DepartmentForm(forms.Form):
    department_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'department_name'})
    )
    
    
    def save(self, institute):
        department_name = self.cleaned_data['department_name']
        department = Department.is_department_exists(department_name, institute)

        if not department:
            return False, "Department already exists!"

        try:
            with transaction.atomic():
                # Create the Institute
                institute = Department.objects.create(
                    department_name=department_name,
                    institute=institute
                )

            return True, "Department created successfully"
        
        except Exception as e:
            return False, f"An error occurred: {e}"