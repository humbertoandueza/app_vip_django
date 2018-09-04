from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
#reverse_lazy
from django.urls import reverse_lazy
#Importo Vistas Genericas para Creacion,Edicion y Eliminar
from django.views.generic.edit import CreateView
#importo El modelo Persona
from .models import Persona
#Importo Formulario
from .forms import PersonaForm
#Importo Mixins Login
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired


# Create your views here.
class PersonasView(LoginRequiredMixin,TemplateView):
	template_name = 'persona/listado.html'

#Retorno Formulario En Json para incrustarlo en Modal
class PersonaCreate(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    model = Persona
    template_name = 'persona/create.html'
    def get(self,request,*args,**kwargs):
        form = PersonaForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

#Class para guardar Persona y en caso de error retorno formulario en Json

class PersonasCreateView(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = PersonaForm(request.POST)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            form = PersonaForm()

        context = {'form': form}
        data['html_form'] = render_to_string('persona/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('persona:personas')



#Funcion Actualizar Persona

def persona_update(request, pk):
    data = dict()
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = PersonaForm(instance=persona)
    context = {'form': form}
    data['html_form'] = render_to_string('persona/update.html',
        context,
        request=request
    )
    return JsonResponse(data)

#Funcion Borrar Persona
def persona_delete(request, pk):
    data = dict()
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        persona.delete()
        data['form_is_valid'] = True
    else:
        context = {'persona':persona}
        data['html_form'] = render_to_string('persona/delete.html',
            context,
            request=request
    )
    return JsonResponse(data)

#Retorno Json para Imprimir con DataTables 
def PersonasJson(request):
    personas = Persona.objects.all()
    json = serializers.serialize('json', personas)
    return HttpResponse(json, content_type='application/json')