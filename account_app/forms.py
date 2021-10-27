from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

Auth_User_Model = get_user_model()


class UserSignupForm(forms.ModelForm):
    """
    User Creation Form
    """
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', }))
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Full Name', }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Password', }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password', }))

    class Meta:
        model = Auth_User_Model
        fields = ('email', 'full_name', 'password1', 'password2')

    def clean_password1(self):
        """
        Verifies password complexity
        """
        password1 = str(self.cleaned_data.get("password1"))
        if len(password1) < 6:
            raise ValidationError(
                "Password is too short, try 8 Characters Long Ones")
        if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{6,}', password1):
            raise ValidationError("Password is too simple, try Complex Ones")
        return password1

    def clean_password2(self):
        """
        Verify If Both passwords Matched
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]
        full_name = self.cleaned_data["full_name"]
        password = self.cleaned_data["password1"]
        if commit:
            user = Auth_User_Model.objects.create_user(
                email=email,
                full_name=full_name,
                password=password)
        return user


class UserLoginForm(forms.Form):
    """
    User Login Form
    """
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'Password', }))


class UserProfileUpdateForm(forms.ModelForm):
    """
    User Profile Update form
    """
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'readonly': 'readonly'}))
    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Full Name', }))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contact Number', }))
    profile_image = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = Auth_User_Model
        fields = ('email', 'full_name', 'phone', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].readonly = True


class UserUpdateAdminForm(forms.ModelForm):
    """
    Admin Panel's User update form
    """
    class Meta:
        model = Auth_User_Model
        fields = ('email', 'full_name', 'is_active',
                  'is_staff', 'is_superuser')
