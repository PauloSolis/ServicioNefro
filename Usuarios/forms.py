from django import forms
from .models import *
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    template = 'Usuarios/user_form.html'

    class Meta:
        model = User
        fields = ["groups"]
        exclude = []
        widgets = {
            'groups': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
