from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
# or
# original_submit_row = submit_row


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):  # NEF-8
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': False,
        'show_save_and_continue': False
        })
    return ctx


class CustomUserAdmin(UserAdmin):  # NEF-8
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        return redirect(reverse_lazy('Usuarios:usuarios_editar', kwargs={'pk': obj.id}))


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
