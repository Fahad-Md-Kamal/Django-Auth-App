from django.contrib.auth.models import BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, password, full_name, **kwargs):
        if not email:
            raise ValueError('You must provide an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **kwargs)
        user.is_active = True
        user.set_password(password)
        try:
            user.save()
        except:
            raise ValueError('Sorry!, Could not Create user')

        return user

    def create_superuser(self, email, password, full_name, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self.create_user(email, password, full_name, **kwargs)
