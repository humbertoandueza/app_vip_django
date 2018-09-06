from django.urls import path
from .views import *

diezmo_urlpatterns = ([
    path('ingresos', IndexPageView.as_view(), name="ingresos"),
    path('ingresojson',IngresoJson,name="IngresosJson"),
    path('crear',IngresoCreate.as_view(),name="crear_ingreso"),
    path('post_ingreso',IngresoCreateView.as_view(),name="post_ingreso"),
    path('ingresos/actualizar/<int:pk>/', ingreso_update,name="put_ingreso"),
    #path('borrar/<int:pk>/', persona_delete,name="borrar_persona"),
    path('capital',Capital,name="capital"),

],"diezmo")

