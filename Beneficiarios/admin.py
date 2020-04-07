from django.contrib import admin
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Register your models here.
@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    actions = None
    form = BeneficiarioForm
    exclude = ('fecha_registro', 'jornada')
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['fecha_registro', 'jornada']
        if not request.user.has_perm('Beneficiarios.delete_beneficiario'):
            self.exclude.append('causa_baja')
            self.exclude.append('activo')
        return super(BeneficiarioAdmin, self).get_form(request, obj, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # NEF-31
    def response_change(self, request, obj):
        return redirect(reverse_lazy('Beneficiarios:beneficiario',
                                     kwargs={'pk': obj.id}))


@admin.register(Antecedentes)
class AntecedentesAdmin(admin.ModelAdmin):
    actions = None
    form = AntecedentesForm
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['beneficiario']
        return super(AntecedentesAdmin, self).get_form(request, obj, **kwargs)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # NEF-31
    def response_change(self, request, obj):
        return redirect(reverse_lazy('Beneficiarios:beneficiario',
                                     kwargs={'pk': obj.beneficiario.id}))
