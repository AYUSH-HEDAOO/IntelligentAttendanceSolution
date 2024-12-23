from django import forms
from .models import (
    Department,
    Designation,
    AcademicSection,
    AcademicClass,
    AcademicSession,
)
from core_apps.staffs.models import Staff
from django.db import transaction
from django.contrib.auth import get_user_model
from core_apps.users.models import Role
from django.contrib.auth.hashers import make_password
from core_apps.common.models import RoleType
from core_apps.students.models import Student

AUTH_USER = get_user_model()


class DepartmentForm(forms.Form):
    department_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "department_name"}
        ),
    )

    def save(self, institute):
        department_name = self.cleaned_data["department_name"]
        department = Department.is_department_exists(department_name, institute)

        if department:
            return False, "Department already exists!"

        try:

            Department.objects.create(
                department_name=department_name, institute=institute
            )

            return True, "Department created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class DesignationForm(forms.Form):
    designation_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "designation_name"}
        ),
    )

    def save(self, institute):
        designation_name = self.cleaned_data["designation_name"]
        designation = Designation.is_designation_exists(designation_name, institute)

        if designation:
            return False, "Designation already exists!"

        try:

            Designation.objects.create(
                designation_name=designation_name, institute=institute
            )

            return True, "Designation created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class StaffForm(forms.Form):
    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name"}),
    )
    last_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "last_name"}),
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "email"}),
    )
    password = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "password"}),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "department"}),
        empty_label="Select Department",
    )
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "designation"}),
        empty_label="Select Designation",
    )

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop(
            "institute", None
        )  # Extract the 'institute' argument
        super().__init__(*args, **kwargs)  # Call the parent class initializer

        if self.institute:
            self.fields["department"].queryset = Department.objects.filter(
                is_deleted=False, institute=self.institute
            )
            self.fields["designation"].queryset = Designation.objects.filter(
                is_deleted=False, institute=self.institute
            )

    def save(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        department = self.cleaned_data["department"]
        designation = self.cleaned_data["designation"]

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
                    user=user, institute=self.institute, role_type=RoleType.STAFF
                )

                # Create the Staff
                Staff.objects.create(
                    role=role,
                    department=department,
                    designation=designation,
                    institute=self.institute,
                )

            return True, "Staff created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class StudentForm(forms.Form):
    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name"}),
    )
    last_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "last_name"}),
    )
    email = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "email"}),
    )
    password = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "password"}),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "department"}),
        empty_label="Select Department",
    )
    enrollment = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "enrollment"}),
    )

    def __init__(self, *args, **kwargs):
        self.institute = kwargs.pop("institute", None)
        super().__init__(*args, **kwargs)  # Call the parent class initializer

        if self.institute:
            self.fields["department"].queryset = Department.objects.filter(
                is_deleted=False, institute=self.institute
            )

    def save(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        department = self.cleaned_data["department"]
        enrollment = self.cleaned_data["enrollment"]

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
                    user=user, institute=self.institute, role_type=RoleType.STUDENT
                )

                # Create the Student
                Student.objects.create(
                    role=role,
                    department=department,
                    enrollment_number=enrollment,
                    institute=self.institute,
                )

            return True, "Student created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class AcademicSectionForm(forms.Form):
    section_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "section_name"}),
    )

    def save(self, institute):
        section_name = self.cleaned_data["section_name"]
        academic_section = AcademicSection.is_section_exists(section_name, institute)

        if academic_section:
            return False, "Academic Section already exists!"

        try:

            AcademicSection.objects.create(
                section_name=section_name, institute=institute
            )

            return True, "Academic Section created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class AcademicClassForm(forms.Form):
    class_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "class_name"}),
    )

    def save(self, institute):
        class_name = self.cleaned_data["class_name"]
        academic_class = AcademicClass.is_class_exists(class_name, institute)

        if academic_class:
            return False, "Academic Class already exists!"

        try:

            AcademicClass.objects.create(class_name=class_name, institute=institute)

            return True, "Academic Class created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"


class AcademicSessionForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control", 
            "id": "start_date", 
            "type": "date"  # Ensures the calendar popup is shown
        }),
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            "class": "form-control", 
            "id": "end_date", 
            "type": "date"  # Ensures the calendar popup is shown
        }),
    )

    def save(self, institute):
        start_date = self.cleaned_data["start_date"]
        end_date = self.cleaned_data["end_date"]
        academic_session = AcademicSession.is_session_exists(
            start_date, end_date, institute
        )
        session_name = f"Session ({start_date} - {end_date})"
        if academic_session:
            return False, "Academic Session already exists!"

        try:

            AcademicSession.objects.create(
                session_name=session_name,
                start_date=start_date,
                end_date=end_date,
                institute=institute,
            )

            return True, "Academic Session created successfully"

        except Exception as e:
            return False, f"Something went wrong: {e}"
