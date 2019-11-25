from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Department)
admin.site.register(models.Checking)
admin.site.register(models.Evection)
admin.site.register(models.Leave)
admin.site.register(models.Log)
admin.site.register(models.Announcement)
admin.site.register(models.Overtime)
admin.site.register(models.Salary)
admin.site.register(models.Role)
admin.site.register(models.Permission)
