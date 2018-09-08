from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Actividades
from django.http import JsonResponse

from django.http import HttpResponse

from django.core import serializers
from .forms import ActividadesForm
from django.template.loader import render_to_string

# Create your views here.
class ActividadesView(ListView):
    model = Actividades
    template_name = 'actividades/listado.html'

def ActividadesJson(request):
    actividades = Actividades.objects.all()
    return JsonResponse(actividades,safe=False)

def AactividadesJson(request):
    actividades = Actividades.objects.all()
    json = serializers.serialize('json', actividades)
    return HttpResponse(json, content_type='application/json')

def ActividadesJson(request):
    dicts = []
    actividad = Actividades.objects.all()
    for i in actividad:
        dicts.append({"color":"#00b0f0","id":i.pk,"title":i.nombre,"start":str(i.fecha)+"T"+str(i.hora),"descripcion":i.descripcion,"lugar":i.lugar,"Estatus":i.status.status,"allDay":False})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)


class ActividadCreate(TemplateView):
    model = Actividades
    template_name = 'actividades/create.html'
    def get(self,request,*args,**kwargs):
        form = ActividadesForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class ActividadesCreateView1(TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = ActividadesForm(request.POST)
            print(request.POST['fecha'])
            if form.is_valid():
                data['form_is_valid'] = True
                data['lugar'] = request.POST['lugar']
                data['start'] = str(request.POST['fecha'])+"T"+str(request.POST['hora'])
                data['descripcion'] = request.POST['descripcion']
                data['title'] = request.POST['nombre']
                data['color'] = "#00B0F0"

                actividad = form.save()
                data['id'] = actividad.pk
            else:
                data['form_is_valid'] = False
        else:
            form = ActividadesForm()

        context = {'form': form}
        data['html_form'] = render_to_string('actividades/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('actividades:home')