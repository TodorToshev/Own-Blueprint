from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("blog:blog")
        messages.error(request, 'Registration failed.')
    else:
        form = UserRegistrationForm()
    return render(request, template_name='registration/registration.html', context={'form': form})
