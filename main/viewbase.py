from django.shortcuts import render
from django.views.generic.base import View
from system.mixins.permission import PermissionGroupMixin
from django.contrib.auth.models import User


# Create your views here.

class MainBase(PermissionGroupMixin, View):
    pass


class MainFactory:

    def __init__(self, request):
        """Формируем значение сессии с ключем group в mainmiddleware.py"""
        self.group = request.session['group']['name']
        # self.group = 'admin'

    def get_object_group(self):
        if self.group == 'admin':
            obj = MainAdmin()
        elif self.group == 'hse':
            obj = MainHse()
        elif self.group == 'lst':
            obj = MainListener()
        elif self.group == 'sch':
            obj = MainSchool()
        return obj


class MainAdmin(MainBase):


    def get(self, request):
        text = 'Это главная страница нового проекта для admin'
        daddy = 'Здесь будем эксперементировать с полиморфизмом'
        return render(request, 'main/admin/main.html', {'text': text, 'daddy': daddy, 'id': 2})


class MainHse(MainBase):
    permission_required = ['hse']

    def get(self, request):
        text = 'Это главная страница нового проекта для hse'
        daddy = 'Здесь будем эксперементировать с полиморфизмом'
        return render(request, 'main/hse/main.html', {'text': text, 'daddy': daddy, 'id': 2})


class MainListener(MainBase):
    permission_required = ['lstr']

    def get(self, request):
        text = 'Это главная страница нового проекта для Listener'
        daddy = 'Здесь будем эксперементировать с полиморфизмом'
        return render(request, 'main/listener/main.html', {'text': text, 'daddy': daddy, 'id': 2})


class MainSchool(MainBase):
    permission_required = ['sch']

    def get(self, request):
        text = 'Это главная страница нового проекта для School'
        daddy = 'Здесь будем эксперементировать с полиморфизмом'
        rec = request.session['group']
        return render(request, 'main/school/main.html', {'text': text, 'daddy': daddy, 'id': 2, 'rec': rec})