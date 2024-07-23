from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegistrationForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Handle form data here
            # For example, save user details, send confirmation email, etc.
            
            # For demonstration, we'll just show a success message
            messages.success(request, 'Account created successfully!')
            return redirect(reverse('/'))  # Replace 'success_page' with your success page URL name
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request,"users/login.html",context)
