from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Agar o'zgartirilgan modeldan foydalansangiz

admin.site.register(CustomUser, UserAdmin)
