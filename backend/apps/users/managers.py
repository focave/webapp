from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class UserManager(DefaultUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError(_("The given email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)

        user.save(using=self._db)

        content_type = ContentType.objects.get_for_model(self.model)
        user.user_permissions.add(
            Permission.objects.get(content_type=content_type, codename="view_user"),
            Permission.objects.get(content_type=content_type, codename="change_user"),
            Permission.objects.get(content_type=content_type, codename="delete_user"),
        )

        assign_perm("users.view_user", user, user)
        assign_perm("users.change_user", user, user)
        assign_perm("users.delete_user", user, user)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)
