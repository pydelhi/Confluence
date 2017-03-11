from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserAttendance

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = [field.name for field in User._meta.fields]
    fieldsets = ()


class UserAttendanceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserAttendance._meta.fields]


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAttendance, UserAttendanceAdmin)
