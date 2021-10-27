from django.forms import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserSignupForm, UserUpdateForm

from .models import UserBase


def user_signup_view(request):
    template_name = 'account_app/form.html'
    form = UserSignupForm()

    if request.method == 'POST':
        form_data = UserSignupForm(request.POST)
        if form_data.is_valid():
            try:
                created_user = form_data.save()
                login(request, created_user)
                messages.success(request,
                                 f'{created_user.full_name}! You have been registared & loggedin successfully')
                return redirect(created_user.get_absolute_url())
            except:
                messages.warning(request, 'Sorry! Failed to sign you up')
        else:
            form = UserSignupForm(request.POST)
    context = {
        'form_name': 'Signup Form',
        'form': form,
    }
    return render(request, template_name, context)


def user_signin_view(request):
    template_name = 'account_app/form.html'
    form = UserUpdateForm()
    context = { 
        'form_name': 'Login Form',
        'form': form
    }
    return render(request, template_name, context)

def user_profile(request, pk):
    template_name = 'account_app/profile.html'
    user = get_object_or_404(UserBase, pk=pk)
    print(user.email)
    context = {
        'user': user,
    }
    return render(request, template_name, context)
