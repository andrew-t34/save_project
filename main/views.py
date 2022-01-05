from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .viewbase import MainBase, MainFactory



# Create your views here.

class Main(MainBase):
    permission_required = ['admin', 'lst', 'sch', 'hse']

    def get(self, request):
        factory = MainFactory(request).get_object_group()

        return factory.get(request)
