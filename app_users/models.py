from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager, StudentManager, TeacherManager, SuperuserManager


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "O'qituvchi"
        SUPERUSER = "SUPERUSER", "Superadmin"

    role = models.CharField(
        max_length=10, choices=Types.choices, default=Types.TEACHER)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def get_role(self):
        return self.role.capitalize()

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.role or self.role is None:
            self.role = User.Types.TEACHER

        if not self.password.startswith(('pbkdf2_', 'argon2$', 'bcrypt$', 'sha1$')):
            self.set_password(self.password)

        return super().save(*args, **kwargs)


class Student(User):
    class Meta:
        proxy = True

    objects = StudentManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.STUDENT
        self.is_student = True
        return super().save(*args, **kwargs)


class Teacher(User):
    class Meta:
        proxy = True

    objects = TeacherManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.TEACHER
        self.is_teacher = True
        return super().save(*args, **kwargs)


class Superuser(User):
    class Meta:
        proxy = True

    objects = SuperuserManager()

    def save(self, *args, **kwargs):
        self.type = User.Types.SUPERUSER
        self.is_superuser = True
        return super().save(*args, **kwargs)
