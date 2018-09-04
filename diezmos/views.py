from django.shortcuts import render
from core.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.base import TemplateView
# Create your views here.
class IndexPageView(LoginRequiredMixin,TemplateView):
    def get(self,request,**kwargs):
        return HttpResponse('Usuario logueado '+request.user.first_name )