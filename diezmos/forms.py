from django import forms

from .models import Ingreso,Egreso

class IngresoForm(forms.ModelForm):

    class Meta:
        model = Ingreso
        fields = ('fecha', 
        'monto',
        'numero_trans',
        'persona',
        'tipo_de_pago')

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = (
            'fecha',
            'monto',
            'descripcion',
            'concepto'
        )