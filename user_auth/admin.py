from django.contrib import admin
from .models import SignupInfo


@admin.register(SignupInfo)
class SignupInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'info', 'email_check_status',
                    'is_signup_finished', 'created_at']
