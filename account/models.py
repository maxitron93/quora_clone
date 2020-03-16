from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

class AccountManager(BaseUserManager):
    # Need to override this method. Need to pass in all the required fields.
    def create_user(self, email, password=None):
        # Check for required fields
        if not email:
            raise ValueError('Users must have an email address')

        # If the required fields are present, create and return the account
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Need to override this method. Need to pass in all the required fields.
    def create_superuser(self, email, password=None):
        # This creates a account using the create_user method above
        user = self.create_user(
            email=email,
            password=password,
        )
        # Set all the admin settings to True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        # Save and return the account with the updated admin settings
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                   = models.EmailField(max_length=120, unique=True)
    date_joined             = models.DateTimeField(auto_now_add=True)
    is_active               = models.BooleanField(default=True)
    is_admin                = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # No need to include the username_field or password
    REQUIRED_FIELDS = []

    objects = AccountManager()

    # This is needed in a custom account model. Returns the permission status
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # This is needed in a custom account model. Returns module permission status
    def has_module_perms(self, app_label):
        return True

# Creates an auth token when a new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
