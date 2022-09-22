from django.contrib import admin
from django.db import models
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from g_muso_app.models import CustomUser

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)