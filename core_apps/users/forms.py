from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from core_apps.users.models import Role
from core_apps.institutes.models import Institute
from django.db import models, transaction
from django.contrib.auth import authenticate, login

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")

    error_messages = {
        "duplicate_email": "A user with this email already exists.",
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])


class RegistrationForm(forms.Form):
    institute_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'institute_name'})
    )
    institute_owner_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'institute_owner_name'})
    )
    institute_owner_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'institute_owner_email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'Password'})
    )
    terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'acceptTerms'}),
        required=True
    )
    
    
    def save(self):
        owner_email = self.cleaned_data['institute_owner_email']
        check_email = User.objects.email_validator(email=owner_email)

        if not check_email:
            return False, "Invalid email, please try another email"

        try:
            with transaction.atomic():
                # Create the Institute
                institute = Institute.objects.create(
                    institute_name=self.cleaned_data['institute_name']
                )

                # Split the owner name
                first_name, last_name = self.cleaned_data['institute_owner_name'].split(' ', 1) if " " in self.cleaned_data["institute_owner_name"] else (self.cleaned_data['institute_owner_name'],"")

                # Create the User
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=owner_email,
                    password=make_password(self.cleaned_data['password']),
                )

                # Create the Role
                Role.objects.create(
                    user=user,
                    institute=institute,
                    role_type='owner'
                )

            return True, "Institute and user created successfully"
        
        except Exception as e:
            return False, f"An error occurred: {e}"
    
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'Email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'Password'})
    )

    def make_user_session(self, request):
        username = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
        return user