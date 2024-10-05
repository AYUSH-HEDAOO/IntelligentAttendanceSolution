from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Handle form data here
            status, _message = form.save()
            if status:
                messages.success(request, 'Account created successfully!')
                return redirect(reverse('Login'))  # Replace 'success_page' with your success page URL name
            messages.warning(request, f'{_message}')
            return redirect(reverse('Register'))
        else:
            messages.warning(request, f'{form.errors}')
            return redirect(reverse('Register'))
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request,"users/register.html",context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Handle form data here
            user_session = form.make_user_session(request)
            messages.success(request, f'Welcome {user_session.first_name} {user_session.last_name}!')
            return redirect(reverse('InstituteDashboard'))
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request,"users/login.html",context)


def user_logout(request):
    logout(request)
    messages.info(request,"Logged Out Successfully!")
    return redirect("Login")


