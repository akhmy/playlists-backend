from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_editable = ('is_staff',)
    fieldsets = UserAdmin.fieldsets + (('Misc', {'fields': ('bio',)}),)
