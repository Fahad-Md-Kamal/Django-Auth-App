from django.shortcuts import (render,
                              redirect,
                              get_object_or_404)
from django.contrib.auth import (authenticate, login)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (UserSignupForm,
                    UserProfileUpdateForm,
                    UserLoginForm)
from django.contrib.auth import logout

from .models import UserBase


def user_signup_view(request):
    """
    Handles user's signup functionality.
    """
    template_name = 'account_app/signup.html'
    form = UserSignupForm()

    if request.method == 'POST':
        form_data = UserSignupForm(request.POST)
        if form_data.is_valid():
            # Signup user, If form is valid
            try:
                created_user = form_data.save()
                messages.success(request,
                                 f'{created_user.full_name}. You have been registared successfully')
                # If registared redirect to signin view
                return redirect('user_auth_app:signin_view')
            except:
                messages.warning(request, 'Sorry! Failed to sign you up')
        else:
            form = UserSignupForm(request.POST)
    context = {
        'form_name': 'Signup Form',
        'form': form,
    }
    return render(request, template_name, context)


def user_login_view(request):
    """
    Handles user's Signin functionaly
    """
    # If user is authenticated redirect to it's profile page.
    if request.user.is_authenticated:
        return redirect(request.user.get_absolute_url())

    form = UserLoginForm()
    if request.method == 'POST':
        form_data = UserLoginForm(request.POST)
        # If for is valid try to authenticate user with given credentials
        if form_data.is_valid():
            try:
                email = form_data.cleaned_data['email']
                password = form_data.cleaned_data['password']
                # Authenticate user with the given credentials
                user = authenticate(email=email, password=password)
                if user:
                    # If user is valid login to the system.
                    login(request, user)
                    messages.success(
                        request, f'Welcome Back {user.full_name}!!')
                    # Redirect to their profile view.
                    return redirect(user.get_absolute_url())
                else:
                    messages.warning(
                        request, f'Please provide a valid email/password')
            except:
                messages.warning(
                    request, f'Sorry, Could not log you in. Please try again later.')
        else:
            form = UserLoginForm(request.POST)

    context = {
        'form_name': 'Login Form',
        'form': form
    }
    return render(request, 'account_app/login.html', context)

# Redirect to Login Url if not registered
@login_required(login_url='/')
def user_profile(request, pk):
    """
    Handels user profile view functionality
    """
    user = get_object_or_404(UserBase, id=pk)

    # Populate user update form with user instance and requested data.
    form = UserProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=user)
    if request.method == 'POST':
        try:
            # If success save form data and show success message
            form.is_valid()
            form.save()
            messages.success(
                request, f'{user.full_name} your profile has been updated successfully!')
            return redirect(user.get_absolute_url())
        except:
            # else return the form to profile page for valid input with error message.
            form = UserProfileUpdateForm(request.POST, request.FILES)
            messages.warning(
                request, f'{user.full_name} sorry, Could not update your profile')
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'account_app/profile.html', context)


def user_logout_view(request):
    """
    Logout User from the session
    """
    logout(request)
    messages.warning(request, f'You have been logged out')
    return redirect('user_auth_app:signin_view')
