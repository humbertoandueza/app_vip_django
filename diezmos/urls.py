from django.urls import path
from .views import *

diezmo_urlpatterns = ([
    path('', IndexPageView.as_view(), name="home")

],"diezmo")

