from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Teacher, Student, Superuser


admin.site.unregister(Group)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Superuser)
