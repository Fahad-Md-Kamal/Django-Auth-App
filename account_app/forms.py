from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

Auth_User_Model = get_user_model()


class UserSignupForm(forms.ModelForm):
    """User Creation Form"""

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

    def clean_password2(self):
        """Verify Both passwords Matched"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user = Auth_User_Model.objects.create_user(email=self.cleaned_data["email"],
                                                full_name=self.cleaned_data["full_name"],
                                                password=self.cleaned_data["password1"])
        return user


class UserUpdateForm(forms.ModelForm):
    """User update form"""

    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', }))

    full_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Full Name', }))

    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Contact Number', }))

    class Meta:
        model = Auth_User_Model
        fields = ('email', 'full_name', 'phone')


class UserUpdateAdminForm(forms.ModelForm):
    """User update form for Admin Panel"""

    class Meta:
        model = Auth_User_Model
        fields = ('email', 'is_active', 'is_staff')
