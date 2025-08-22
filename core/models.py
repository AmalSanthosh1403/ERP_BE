from django.db import models
from django.contrib.auth.models import AbstractUser


class Permission(models.Model):
    """
    Permission codes. Example: "user.create", "user.list.any", "employee.list.only", Will be presetted by the script.
    """
    code = models.CharField(max_length=100, unique=True)  # immutable
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "core_permissions"
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"


class Role(models.Model):
    """
    Role groups multiple permissions. Admin/Manager/Employee are just Role records.
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    is_employee = models.BooleanField(default=False)  # Flag to identify employee role
    permissions = models.ManyToManyField(Permission, related_name="roles", blank=True)

    def __str__(self):
        return self.code
    
    class Meta:
        db_table = "core_roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"


class User(AbstractUser):
    """
    Extends Django's built-in user with a Role FK.
    """
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")

    def __str__(self):
        return self.email if self.email else self.username

    class meta:
        db_table = "core_users"
        verbose_name = "User"
        verbose_name_plural = "Users"
