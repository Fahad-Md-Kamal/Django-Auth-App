from django.urls import path
from .views import (user_signup_view, user_login_view, user_profile, user_logout_view)


app_name = 'user_auth_app'

urlpatterns = [
    path('sign-up/', user_signup_view, name='signup_view' ),
    path('sign-in/', user_login_view, name='signin_view' ),
    path('profile/<int:pk>/', user_profile, name='profile_view' ),
    path('logout/', user_logout_view, name='logout_view' ),
]
