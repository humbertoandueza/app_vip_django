from django.urls import path
from .views import *

diezmo_urlpatterns = ([
    #Url para ingresos
    path('ingresos', IndexPageView.as_view(), name="ingresos"),
    path('ingresojson',IngresoJson,name="IngresosJson"),
    path('crear_ingreso',IngresoCreate.as_view(),name="crear_ingreso"),
    path('post_ingreso',IngresoCreateView.as_view(),name="post_ingreso"),
    path('ingresos/actualizar/<int:pk>/', ingreso_update,name="put_ingreso"),

    #Url para Egresos
    path('egresos', IndexEgresoPageView.as_view(), name="egresos"),
    path('egresojson',EgresoJson,name="EgresosJson"),
    path('crear_egreso',EgresoCreate.as_view(),name="crear_egreso"),
    path('post_egreso',EgresoCreateView.as_view(),name="post_egreso"),
    path('capital',Capital,name="capital"),

],"diezmo")

