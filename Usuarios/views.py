from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User, Group, Permission
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class UserUpdate(PermissionRequiredMixin, UpdateView):  # NEF-8
    permission_required = "auth.change_user"
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse_lazy('admin:auth_user_changelist')

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['usuario'] = User.objects.get(id=self.kwargs['pk'])
        return context
