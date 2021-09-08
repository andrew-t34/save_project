from django.shortcuts import render
from .models import *
from django.views.generic.base import View
from .factory import Configurator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from system.mixins.permission import PermissionGroupMixin
from dal import autocomplete
from django.core.paginator import Paginator
from django.http import request


# Create your views here.
class BaseController:
    _class_name = ''

    def __init__(self, *args, **kwargs):
        if self._class_name:
            self.configurator = Configurator(self._class_name)
        super().__init__(*args, **kwargs)

    def get_obj(self, request, kwargs=''):
        """request - это данные из request. Приходят из функции get класса (объекта)"""
        obj = self.configurator.get_object_group(request)
        """configurator - получаем из factory см. метод init"""
        if 'factory' in kwargs:
            """Проверяем есть ли метко для выбора фабрики. Передается через URL"""
            if kwargs['factory'] in obj.permission_list_of_factories:
                """permission_list_of_factories - перечень фабрик доступных для группы пользователей"""
                """представлен в файле этой группы папки access_view"""
                factory_obj = obj.select_form_factory(request=request, keys=kwargs)
                """создали и вернули объект конкретной фабрики в зависимости от названия в kwargs"""
                """сам метод select_form_factory находится в родительском классе полученного обекта obj"""
                return factory_obj
            """Если фабрики форм нет возвращаем объект соответствуещей группы из factory.py"""
        return obj


class MainStudy(PermissionGroupMixin, BaseController, View):
    permission_required = ['admin', 'sch', 'listener']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request):
        obj = self.get_obj(request)
        return render(request, obj.template, {
            'level_count': obj.level_data.count(),
            'field_count': obj.field_data.count(),
            'program_count': obj.program_data.count(),
            'topic_count': obj.topic_data.count()
        })


class CreateUpdateController(PermissionGroupMixin, BaseController, View):
    permission_required = ['admin', 'sch']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Важно!!! Передача реквест и кваргс поволяет внутри фабрики работать с этими данными"""
        obj = self.get_obj(request, kwargs)
        if 'delete' in kwargs:
            obj.model.del_data()
            return HttpResponseRedirect(reverse(obj.redirect_url, kwargs=obj.kwargs_redirect))
        form = obj.form.get_form()
        return render(request, obj.template_form, {
            'form': form,
            'kwargs': kwargs,
        })

    def post(self, request, **kwargs):
        obj = self.get_obj(request, kwargs)
        form = obj.form.get_form()
        if form.is_valid():
            obj.model.make_save(form.cleaned_data)
            return HttpResponseRedirect(reverse(obj.redirect_url, kwargs=obj.kwargs_redirect))
        else:
            return render(request, obj.template_form, {
                "form": form,
                'kwargs': kwargs})


class ListUnit(PermissionGroupMixin, BaseController, View):
    permission_required = ['admin', 'sch']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_obj(request, kwargs)
        return render(request, obj.chosen_factory.template_list, {
            'units': obj.chosen_factory.list.get_list(),
            'kwargs': kwargs,
        })


class ProgramDetail(PermissionGroupMixin, BaseController, View):
    permission_required = ['admin', 'sch', 'listener']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_obj(request, kwargs)
        program = Program.objects.get(id=kwargs['program_id'])
        modules = program.modules.all().values()
        topics = Topic.objects.filter(program_id=kwargs['program_id']).values()
        paginator = Paginator(topics, 1)
        page_number = request.GET.get('page')
        return render(request, obj.template, {'kwargs': kwargs,
                                              'program': program,
                                              'modules': modules,
                                              'topics': topics,
                                              'topic_obj': paginator.get_page(page_number)})


class LevelAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Level.objects.none()
        qs = Level.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class FieldAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Field.objects.none()
        qs = Field.objects.all()
        level = self.forwarded.get('level', None)
        if level:
            qs = qs.filter(level=level)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class ModuleAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Module.objects.none()
        qs = Module.objects.all()
        program = self.forwarded.get('program_id', None)
        if program:
            qs = qs.filter(program_id=program)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs