from django.shortcuts import render, get_object_or_404,redirect
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum
import  json
from django.views.generic.base import TemplateView

#Importo El model
from .models import Ingreso,Egreso
#Importo Form
from .forms import IngresoForm
from django.template.loader import render_to_string
# Create your views here.
class IndexPageView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'diezmos/ingreso/listado.html')

#Retorno Json para Imprimir con DataTables
def IngresoJson(request):
    dicts = []
    monto = Ingreso.objects.aggregate(Sum('monto'))
    ingresos = Ingreso.objects.all()
    for i in ingresos:
        dicts.append({"model":"model.ingreso","pk":i.pk,"fields":{"fecha":i.fecha,"monto":str(i.monto)+" bs.","numero_trans":i.numero_trans,"cedula":i.persona.cedula,"persona":i.persona.nombre,"tipo_de_pago":i.tipo_de_pago.tipopago}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)

#Formulario del modelo Ingresos

class IngresoCreate(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    model = Ingreso
    template_name = 'diezmos/ingreso/create.html'
    def get(self,request,*args,**kwargs):
        form = IngresoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

#Class Post Ingresos
class IngresoCreateView(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = IngresoForm(request.POST)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False
        else:
            form = IngresoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/ingreso/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('diezmo:home')
#Funcion para Actualizar

#Retorno Json Capital Disponible
def Capital(request):
    montoingreso = Ingreso.objects.aggregate(Sum('monto'))
    montoegreso = Egreso.objects.aggregate(Sum('monto'))
    if montoingreso['monto__sum'] == None or montoegreso['monto__sum'] == None:
        capital = {"capital":0}

        if montoingreso['monto__sum'] != None:
            capital = {"capital":montoingreso['monto__sum']}
        elif montoegreso['monto__sum'] != None:
            capital = {"capital":-montoegreso['monto__sum']}
    else:
        capital = {"capital":(montoingreso['monto__sum'] - montoegreso['monto__sum'])}
    return JsonResponse(capital)

#Funcion para obtener el capital
def capital_obtener():
    montoingreso = Ingreso.objects.aggregate(Sum('monto'))
    montoegreso = Egreso.objects.aggregate(Sum('monto'))
    if montoingreso['monto__sum'] == None or montoegreso['monto__sum'] == None:
        capital = 0
        if montoingreso['monto__sum'] != None:
            capital = montoingreso['monto__sum']
        elif montoegreso['monto__sum'] != None:
            capital = montoegreso['monto__sum']
    else:
        capital = (montoingreso['monto__sum'] - montoegreso['monto__sum'])
    return capital


def ingreso_update(request, pk):
    data = dict()
    ingreso = get_object_or_404(Ingreso, pk=pk)
    if request.method == 'POST':
        montoegreso = int(capital_obtener())
        monto_actualizar = int(request.POST['monto'])
        resta = (int(ingreso.monto)-montoegreso)
        resta2 = monto_actualizar-resta
        print ("\n \n \n \n resta",resta2)
        form = IngresoForm(request.POST, instance=ingreso)

        if resta2 < 0:
            data['error'] = "El monto que intenta actualizar es no coincide con el dinero disponible"
            print (data['error'])
            data['form_is_valid'] = False
        else:
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True

            else:
                data['form_is_valid'] = False
        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/ingreso/update.html',
            context,
            request=request
        )
        return JsonResponse(data)
    else:
        form = IngresoForm(instance=ingreso)
    context = {'form': form}
    data['html_form'] = render_to_string('diezmos/ingreso/update.html',
        context,
        request=request
    )
    return JsonResponse(data)