from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
          Group,
          related_name="customuser_set",  # Change the related name
          blank=True,
          help_text="The groups this user belongs to.",
          verbose_name="groups",
      )
    user_permissions = models.ManyToManyField(
          Permission,
          related_name="customuser_permissions",  # Change the related name
          blank=True,
          help_text="Specific permissions for this user.",
          verbose_name="user permissions",
      )
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    passcode = models.CharField(max_length=128)  # Hashed version
    bvn = models.CharField(max_length=11, blank=True, null=True)
    nin = models.CharField(max_length=11, blank=True, null=True)
    photograph = models.ImageField(upload_to='photographs/', blank=True, null=True)
    biometrics = models.TextField(blank=True, null=True)  # Store optional biometric data
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state_of_origin = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    authentication_stage = models.PositiveIntegerField(default=1)

    def generate_email_verification_code(self):
        self.email_verification_code = get_random_string(6, allowed_chars='0123456789')
        self.save()
      # Tracks the current stage

# Create your models here.

