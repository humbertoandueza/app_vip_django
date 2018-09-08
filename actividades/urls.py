from django.urls import path
from .views import *

actividades_urlpatterns = ([
    path('', ActividadesView.as_view(), name="home"),
    path('actividades', ActividadesJson, name="actividades_json"),
    path('crear',ActividadCreate.as_view(),name="crear_actividad"),
    path('post',ActividadesCreateView1.as_view(),name="post_actividad")

],"actividades")

