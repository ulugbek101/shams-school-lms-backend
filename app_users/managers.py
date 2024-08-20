from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required.")
        if not password:
            raise ValueError("Password is must.")

        from .models import User  # Import model here, lazily
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset()


class StudentManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)


class TeacherManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class SuperuserManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=True)
