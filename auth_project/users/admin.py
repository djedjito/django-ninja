from django.contrib import admin

from .models import CustomUser, Profile, MenuItem, UserPermission

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(MenuItem)
admin.site.register(UserPermission)