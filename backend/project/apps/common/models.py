from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# custom user model for authentication and signup on the web app
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self.create_user(email, password=password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50,unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)

    # Status & permissions
    is_email_notification = models.BooleanField(default=False) 
    is_mobile_notification = models.BooleanField(default=False) 

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __str__(self):
        return self.email





# Service Provider

class ServiceProvider(models.Model):
    PROVIDER_TYPE = [
        ('flight', 'Flight'),
        ('hotel', 'Hotel'),
        ('cab', 'Cab'),
    ]

    owner = models.ForeignKey(User,on_delete=models.CASCADE) 

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPE)
   
    logo = models.ImageField(upload_to='service_providers/', null=True, blank=True)
    country = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    gstin_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.provider_type})"





