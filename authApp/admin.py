from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BeaconUser, BeaconDevice

@admin.register(BeaconUser)
class BeaconUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(BeaconDevice)
class BeaconDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'major', 'minor', 'created_by', 'is_active')
    search_fields = ('name', 'uuid')
    list_filter = ('is_active', 'created_at')