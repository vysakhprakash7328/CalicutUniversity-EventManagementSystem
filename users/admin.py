from django.contrib import admin

from users.models import DepartmentHead, Department

# Register your models here.

admin.site.register(DepartmentHead)
admin.site.register(Department)
