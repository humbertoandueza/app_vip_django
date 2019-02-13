from django.shortcuts import render, get_object_or_404,redirect
from core.mixins import LoginRequiredMixin,SuperUserMixinRequired
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Sum
from datetime import datetime
import  json
from django.views.generic.base import TemplateView

#Importo El model
from .models import Ingreso,Egreso
#Importo Form
from .forms import IngresoForm,EgresoForm
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
def consulta(request):
    query = Ingreso.objects.aggregate(Sum('monto'))
    return render(request,plantillaHtml,{'context':query})
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
def ofrenda():
    MesActual = datetime.now().month
    montoofrenda = Ingreso.objects.filter(persona__nombre='Ofrenda',fecha__month=MesActual).aggregate(Sum('monto'))
    if montoofrenda['monto__sum'] == None:
        montoofrenda = 0
    else:
        montoofrenda = montoofrenda['monto__sum']
    return (montoofrenda)
#Retorno Json Capital Disponible
def Capital(request):
    MesActual = datetime.now().month

    montoingreso = Ingreso.objects.aggregate(Sum('monto'))
    montoingreso_mes = Ingreso.objects.filter(fecha__month=MesActual).aggregate(Sum('monto'))

    montoegreso = Egreso.objects.aggregate(Sum('monto'))

    #obtener valores de ofrenda
    if montoingreso['monto__sum'] == None or montoegreso['monto__sum'] == None:
        capital = {"total":0,"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":0}

        if montoingreso['monto__sum'] != None:
            capital = {"total":montoingreso['monto__sum'],"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":montoingreso_mes['monto__sum']-ofrenda()}
        elif montoegreso['monto__sum'] != None:
            capital = {"total":-total['monto__sum'],"ofrenda":ofrenda(),"ofrenda":ofrenda(),"diezmo":montoingreso_mes['monto__sum']-ofrenda()}
    else:
        resta = int(montoingreso['monto__sum'] - montoegreso['monto__sum'])
        if montoingreso_mes['monto__sum'] == None:
            montoingreso_mes = 0
        else:
            montoingreso_mes = montoingreso_mes['monto__sum']
        print (montoingreso_mes)
        resta_mes = int(montoingreso_mes-ofrenda())
        capital = {"total":resta,"ofrenda":ofrenda(),"diezmo":resta_mes}
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

#Funcion para actualizar
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



# Index del Egreso
class IndexEgresoPageView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        return render(request,'diezmos/egreso/listado.html')

#Retorno Json para Imprimir con DataTables
def EgresoJson(request):
    dicts = []
    monto = Egreso.objects.aggregate(Sum('monto'))
    egresos = Egreso.objects.all()
    for i in egresos:
        dicts.append({"model":"model.egreso","pk":i.pk,"fields":{"fecha":i.fecha,"monto":str(i.monto)+" bs.","descripcion":i.descripcion,"concepto":i.concepto.concepto}})
    #print ('dictionario: ',dicts)

    #json = serializers.serialize('json', dicts)
    return JsonResponse(dicts,safe=False)


#Class Formulario Egreso
class EgresoCreate(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    model = Egreso
    template_name = 'diezmos/egreso/create.html'
    def get(self,request,*args,**kwargs):
        form = EgresoForm()
        context = {'form': form}
        html_form = render_to_string(self.template_name,
        context,
        request=request)
        return JsonResponse({'html_form': html_form})

class EgresoCreateView(LoginRequiredMixin,SuperUserMixinRequired,TemplateView):
    def post(self,request,*args,**kwargs):
        data = dict()
        
        if request.method == 'POST':
            form = EgresoForm(request.POST)
            capital = int(capital_obtener())
            monto_egreso = int(request.POST['monto'])
            resta = (capital-monto_egreso)
            print ("\n \n \n \n resta",resta)

            if resta < 0:
                data['error'] = "El monto que intenta retirar es no coincide con el dinero disponible"
                print (data['error'])
                data['form_is_valid'] = False
            else:
                if form.is_valid():
                    usuario = form.save(commit=False)
                    usuario.usuario = request.user
                    form.save()
                    data['form_is_valid'] = True

                else:
                    data['form_is_valid'] = False
            context = {'form': form}
            data['html_form'] = render_to_string('diezmos/egreso/create.html',
                context,
                request=request
            )
            return JsonResponse(data)
        else:
            form = EgresoForm()

        context = {'form': form}
        data['html_form'] = render_to_string('diezmos/egreso/create.html',
            context,
            request=request)
        return JsonResponse(data)
    def  get(self,request):
        return redirect('diezmo:home')
