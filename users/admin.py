from django.contrib import admin
from django.contrib.auth import get_user_model
# from .models import Moderator


CustomUser = get_user_model()

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number','first_name', 'last_name', 'is_moderator',)

admin.site.register(CustomUser, CustomUserAdmin)
