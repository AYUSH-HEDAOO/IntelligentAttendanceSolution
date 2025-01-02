from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from core_apps.students.models import  Attendance

AUTH_USER = get_user_model()


class AttendanceForm(forms.Form):
    enter_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control", 
            "id": "enter_date", 
            "type": "date"  # Ensures the calendar popup is shown
        }),
    )
    in_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            "class": "form-control", 
            "id": "enter_date", 
            "type": "time"  # Ensures the time popup is shown
        }),
    )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        self.institute = self.current_user.institute
        super().__init__(*args, **kwargs)  # Call the parent class initializer


    def save(self):
        enter_date = self.cleaned_data["enter_date"]
        in_time = self.cleaned_data["in_time"]
        
        try:
            with transaction.atomic():

                created_by_uuid_role = f"{self.current_user.user.id}/{self.current_user.role_type}"
                # Create the Student
                Attendance.objects.create(
                    a_date=enter_date,
                    a_in_time=in_time,
                    institute=self.institute,
                    created_by_uuid_role=created_by_uuid_role
                )

            return True, "Student created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"
