from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class BeaconUser(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('OPERATOR', 'Operator'),
        ('VIEWER', 'Viewer'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='VIEWER')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class BeaconDevice(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    major = models.IntegerField()
    minor = models.IntegerField()
    created_by = models.ForeignKey(BeaconUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.uuid}"