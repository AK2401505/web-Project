from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Task,users


admin.site.register(Task)
admin.site.register(users, UserAdmin)
