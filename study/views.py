from django.shortcuts import render
from .models import *
from django.views.generic.base import View
from .factory import Configurator
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from system.mixins.permission import PermissionGroupMixin
from dal import autocomplete
from system.controller import BaseController
from validators import url


class MainStudy(PermissionGroupMixin, BaseController, View):
    permission_required = ['admin', 'sch', 'lst']

    def __init__(self, *args, **kwargs):
        self.conf = BaseController(class_name=self.__class__.__name__, configurator=Configurator)

    def get(self, request, **kwargs):
        obj = self.conf.get_obj(request, kwargs)
        return render(request, obj.template, obj.get_data())


class CreateUpdateController(PermissionGroupMixin, View):
    permission_required = ['admin', 'sch']

    def __init__(self, *args, **kwargs):
        self.conf = BaseController(class_name=self.__class__.__name__, configurator=Configurator)
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Важно!!! Передача реквест и кваргс поволяет внутри фабрики работать с этими данными"""
        obj = self.conf.get_obj(request, kwargs)
        if 'delete' in kwargs:
            obj.model.del_data()
            if 'HTTP_REFERER' in request.META and url(request.META.get('HTTP_REFERER'), public=False):
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            return HttpResponseRedirect(reverse(obj.redirect_url, kwargs=obj.kwargs_redirect))
        form = obj.form.get_form()
        return render(request, obj.template_form, {
            'form': form,
            'kwargs': kwargs,
        })

    def post(self, request, **kwargs):
        obj = self.conf.get_obj(request, kwargs)
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
        self.conf = BaseController(class_name=self.__class__.__name__, configurator=Configurator)

    def get(self, request, **kwargs):
        obj = self.conf.get_obj(request, kwargs)
        return render(request, obj.list.template_list, {
            'units': obj.list.get_list(),
            'kwargs': kwargs,
            'form': obj.list.get_filter_form() if hasattr(obj.list, 'get_filter_form') else False
        })


class ProgramDetail(PermissionGroupMixin, View):
    permission_required = ['admin', 'sch', 'lst']
    topics = False
    topic = False
    topic_num = False
    topic_nums = False
    next_topic = False
    previous_topic = False
    module_list = False

    def __init__(self, *args, **kwargs):
        self.module_list = []
        self.obj = False
        self.conf = BaseController(class_name=self.__class__.__name__, configurator=Configurator)

    def get(self, request, **kwargs):
        self.obj = self.conf.get_obj(request, kwargs)
        self.get_topics()
        if self.topics:
            if 'topic_id' in self.obj.data_url:
                self.topic = Topic.objects.filter(id=self.obj.data_url['topic_id']).select_related('module', 'program')[0]
            else:
                self.topic = self.topics[0]
            self.get_nums()
            for module in self.topics:
                self.module_list.append(module.module)
            self.module_list = list(set(self.module_list))
        else:
            """При формировании нового модуля он не отображается пока не создадут тему """
            """для данного модуля."""
            if self.obj.module_data.filter(program_id=self.obj.data_url['program_id']):
                self.module_list = True
        return render(request, self.obj.template, {'kwargs': kwargs,
                                                   'modules': self.module_list,
                                                   'topics': self.topics,
                                                   'topic': self.topic,
                                                   'next_topic': self.next_topic,
                                                   'previous_topic': self.previous_topic,
                                                   'topic_nums': self.topic_nums,
                                                   'topic_num': self.topic_num+1
                                                   })

    def get_topics(self):
        self.topics = self.obj.topic_data.filter(
            program_id=self.obj.data_url['program_id']).select_related(
            'module', 'program').order_by(
            'module')

    def get_nums(self):
        if self.topics:
            self.topic_num = list(self.topics).index(self.topic)
            self.topic_nums = len(self.topics)
            if len(self.topics) != self.topic_num + 1:
                self.next_topic = self.topics[self.topic_num + 1]
            if self.topic_num != 0:
                self.previous_topic = self.topics[self.topic_num - 1]


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


class TopicAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Topic.objects.none()
        qs = Topic.objects.all()
        module = self.forwarded.get('module_id', None)
        if module:
            qs = qs.filter(module_id=module)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs
