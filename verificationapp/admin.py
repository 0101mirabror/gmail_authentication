from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Profile)

class CustomUserAdmin(UserAdmin):
    
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields':( )}),
    )
    list_display = [
        "id",
        "email",
        "username",
        "is_superuser",
        "is_staff",
         
    ]  

admin.site.register(CustomUser, CustomUserAdmin)
 