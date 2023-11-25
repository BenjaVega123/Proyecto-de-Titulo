from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from applications.user.models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('password', 'RUT', 'username')}),
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        (None, {'fields': ('asking_rol', 'rol', 'telefono','carrera','nrcs')}),
    )

    ordering = ('id',)

    list_display = (
                       'id',
                   ) + BaseUserAdmin.list_display

    search_fields = (
        'id',
        'first_name',
        'last_name',
        'email',
        'RUT',
        'rol'
    )


admin.site.register(User, UserAdmin)
