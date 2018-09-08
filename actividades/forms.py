from django import forms

from .models import *
import datetime

class ActividadesForm(forms.ModelForm):


    class Meta:
        model = Actividades
        fields = ('nombre','descripcion','lugar','persona','status','tipo','fecha','hora')
        widget = {
            'hora':forms.TimeField(),
        }

    def __init__(self,*args,**kwargs):
        super (ActividadesForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['persona'].queryset = Persona.objects.filter(roles="Lider")
