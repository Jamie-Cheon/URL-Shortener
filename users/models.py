
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

MEMBERSHIP_CHOICES = (
    (0, 'VIP'),
    (1, 'NORMAL'),
)


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    A manager is an interface through which database query operations are provided to Django models.
    """

    def _create_user(self, email, username, password, membership=1, **extra_fields):
        """
        Create and save a user with the given email, username and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, membership=membership, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Use an email address as the primary user identifier instead of a username for authentication
    """
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)    # Made the email field unique

    username = models.CharField(max_length=30, null=True)
    membership = models.SmallIntegerField(choices=MEMBERSHIP_CHOICES, null=True)
    created = models.DateTimeField(default=timezone.now)

    objects = UserManager()   # Replace the default model manager with custom UserManager
    USERNAME_FIELD = 'email'  # Set the USERNAME_FIELD (which defines the unique identifier for the User model) to email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email