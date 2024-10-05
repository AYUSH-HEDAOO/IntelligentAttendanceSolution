from django.shortcuts import render,redirect
from django.urls import reverse
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
            messages.success(request, 'You logged in successfully!')
            return redirect(reverse('/institute/dashboard'))  # Replace 'success_page' with your success page URL name
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request,"users/login.html",context)





