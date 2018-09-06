from django import forms

from .models import Ingreso

class IngresoForm(forms.ModelForm):

    class Meta:
        model = Ingreso
        fields = ('fecha', 
        'monto',
        'numero_trans',
        'persona',
        'tipo_de_pago')

    