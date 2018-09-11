from django.urls import path
from .views import *

actividades_urlpatterns = ([
    path('', ActividadesView.as_view(), name="home"),
    path('actividades', ActividadesJson, name="actividades_json"),
    path('crear',ActividadCreate.as_view(),name="crear_actividad"),
    path('post',ActividadesCreateView1.as_view(),name="post_actividad"),
    path('actualizar/<int:pk>/', Status_update,name="actualizar_status"),
    path('chart',chart,name="chart"),
    path('estadisticas',EstadisticasView.as_view(),name="estadisticas")


],"actividades")

