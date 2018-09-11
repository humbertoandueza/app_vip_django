from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Actividades,Status
from django.http import JsonResponse

from django.http import HttpResponse

from django.core import serializers
from .forms import ActividadesForm,StatusForm
from django.template.loader import render_to_string
from datetime import datetime
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
        if i.status.status == 'Suspendida':
            color = "#ffc100"
        if i.status.status == 'Realizada':
            color = "green"
        if i.status.status == 'Por Realizar':
            color = "#00B0F0"
        if i.status.status == 'No Realizada':
            color = "red"
        dicts.append({"color":color,"id":i.pk,"title":i.nombre,"start":str(i.fecha)+"T"+str(i.hora),"descripcion":i.descripcion,"lugar":i.lugar,"estatus":i.status.status,"allDay":False})
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
        estatus_id = get_object_or_404(Status,status="Por Realizar")
        if request.method == 'POST':
            form = ActividadesForm(request.POST)
            print(request.POST['fecha'])
            if form.is_valid():
                data['form_is_valid'] = True
                data['lugar'] = request.POST['lugar']
                data['start'] = str(request.POST['fecha_submit'])+"T"+str(request.POST['hora'])
                data['descripcion'] = request.POST['descripcion']
                data['title'] = request.POST['nombre']
                data['color'] = "#00B0F0"
                status_p = form.save(commit=False)
                status_p.status = estatus_id
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


def Status_update(request, pk):
    data = dict()
    estatus = get_object_or_404(Actividades, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=estatus)
        fecha = ''
        for i in request.POST:
            print (request.POST)
            if i == 'fecha_submit':
                estatus_id = get_object_or_404(Status,status="Por Realizar")
                fecha = request.POST['fecha_submit']
                hora = request.POST['hora']
                print ('obtengo la fecha a actualizar ',fecha )
        if fecha:
            #Nuevo registro
            if estatus.entrenamiento:
                entrenamiento= estatus.entrenamiento
            else:
                entrenamiento = None
            estatus.suspended = True
            estatus.save()
            actividad_new = Actividades(nombre = estatus.nombre,descripcion = estatus.descripcion,fecha=fecha,hora=hora,lugar = estatus.lugar,persona = estatus.persona,status = estatus_id,tipo = estatus.tipo,entrenamiento=entrenamiento)
            actividad_new.save()
            data['id'] = actividad_new.pk
            status_p = form.save(commit=False)
            data['create'] =True
            data['lugar'] = estatus.lugar
            data['descripcion'] = estatus.descripcion
            data['title'] = estatus.nombre
            data['color'] = "#00B0F0"
            data['start'] = str(fecha)+"T"+str(hora)
            data['estatus'] = estatus_id.status
            data['form_is_valid'] = True

        else:
            if form.is_valid():
                form.save()
                if estatus.status.status == 'Suspendida':
                    color = "#ffc100"
                    print ("Suspendida")
                if estatus.status.status == 'Realizada':
                    color = "green"
                    print (color)
                if estatus.status.status == 'Por Realizar':
                    color = "#00B0F0"
                if estatus.status.status == 'No Realizada':
                    color = "red"

                data['form_is_valid'] = True
                data['color'] = color
                data['estatus'] = estatus.status.status
    else:
        form = StatusForm(instance=estatus)
    context = {'form': form,'actividad':estatus}
    data['html_form'] = render_to_string('actividades/update.html',
        context,
        request=request
    )
    return JsonResponse(data)

def chart(request):
    data = []
    MesActual = datetime.now().month-1
    activividades = Actividades.objects.filter(fecha__month=MesActual).exclude(status__status="Por Realizar").count()
    suspendida = Actividades.objects.filter(status__status="Suspendida",fecha__month=MesActual).count()
    realizada = Actividades.objects.filter(status__status="Realizada",fecha__month=MesActual).count()
    no_realizada = Actividades.objects.filter(status__status="No Realizada",fecha__month=MesActual).count()
    if suspendida:
        por_sus = (100*suspendida)/activividades
        data.append({"value": round(por_sus, 2),"label":"Suspendidas"})
    if realizada:
        por_rea = (100*realizada)/activividades
        data.append({"value": round(por_rea, 2),"label":"Realizadas"})
    if no_realizada:
        por_no_rea = (100*no_realizada)/activividades
        data.append({"value": round(por_no_rea, 2),"label":"No Realizadas"})

    return JsonResponse(data,safe=False)


class EstadisticasView(TemplateView):
    template_name = 'actividades/estadisticas.html'