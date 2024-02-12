from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Address

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, AddressInline)

    list_display = ('email', 'username', 'is_active', 'is_staff', 'role')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('email', 'username')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'edited_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff', 'role', 'groups', 'user_permissions'),
        }),
    )

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'street', 'city', 'state', 'postal_code', 'country', 'user')
    search_fields = ('street', 'city', 'state', 'postal_code', 'country', 'user__email', 'user__username')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)

