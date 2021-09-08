from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from .factory import KnowledgeConfigurator
from django.urls import reverse
from django.http import Http404
from system.mixins.permission import PermissionGroupMixin
from django.forms import formset_factory
from .models import *

# Create your views here.


class ProgramQuestions(PermissionGroupMixin, View):
    class_name = 'ProgramQuestions'
    permission_required = ['admin']

    def __init__(self, *args, **kwargs):
        self._configurator = KnowledgeConfigurator()
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self._configurator.get_object_group(request, self.class_name)
        data = obj.select_questions(kwargs)
        return render(request, obj.template, {'programs': data['programs'],
                                              'modules': data['modules'],
                                              'questions': data['questions'],
                                              'count_questions': data['count_questions'],
                                              'kwargs': kwargs})


class CreateUpdateForm(PermissionGroupMixin, View):

    class_name = 'CreateUpdateForm'
    permission_required = ['admin']

    def __init__(self, *args, **kwargs, ):
        self.configurator = KnowledgeConfigurator()
        self.model_obj_for_form = False
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Получаем объект для конкретной группы пользователей"""
        obj = self.configurator.get_object_group(request, self.class_name)
        """Проверяем есть ли доступ к форме создания раздела для этого пользователя"""
        if kwargs['form_name'] in obj.perm_list_form_factories:
            obj.select_form_factory(kwargs['form_name'])
            if 'pk' in kwargs:
                """Получаем данные из таблицы по id записи"""
                self.model_obj_for_form = obj.chosen_factory.model.get_model_id(kwargs['pk'])
            form = obj.chosen_factory.form.get_form(self.model_obj_for_form, kwargs)
            """кастыль!!!!!!!!!"""
            answers = ''
            if kwargs['form_name'] == 'answer':
                answers = obj.select_answers(kwargs['question_id'])

            return render(request, obj.chosen_factory.template_form, {'form': form,
                                                                      'kwargs': kwargs,
                                                                      'answers': answers})
        return Http404()

    def post(self, request, **kwargs):
        obj = self.configurator.get_object_group(request, self.class_name)
        if kwargs['form_name'] in obj.perm_list_form_factories:
            obj.select_form_factory(kwargs['form_name'])
            form = obj.chosen_factory.form.get_form(request.POST)
            return self.form_validate(request, obj, form, kwargs)
        return Http404

    def form_validate(self, request, obj, form, kwargs):
        pass


class CreateUpdateFormAnswer(CreateUpdateForm):

    def form_validate(self, request, obj, form, kwargs):
        answers = obj.select_answers(kwargs['question_id'])
        if form.is_valid():
            obj.chosen_factory.model.make_save_model(form.cleaned_data)
            return HttpResponseRedirect(reverse('cr_up_answer',
                                                kwargs=kwargs))
        else:
            return render(request, obj.chosen_factory.template_form, {'form': form,
                                                                      'kwargs': kwargs,
                                                                      'answers': answers})


class CreateUpdateFormQuestion(CreateUpdateForm):

    def form_validate(self, request, obj, form, kwargs):
        if form.is_valid():
            obj.chosen_factory.model.make_save_model(form.cleaned_data)
            return HttpResponseRedirect(reverse('program_questions', kwargs={'program_id': kwargs['program_id']}))
        else:
            return render(request, obj.chosen_factory.template_form, {'form': form,
                                                                      'kwargs': kwargs})


class DeleteData(PermissionGroupMixin, View):

    permission_required = ['admin']
    class_name = 'DeleteData'

    def __init__(self, *args, **kwargs, ):
        self.configurator = KnowledgeConfigurator()
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.configurator.get_object_group(request, self.class_name)
        if kwargs['form_name'] in obj.perm_list_form_factories:
            obj.select_form_factory(kwargs['form_name'])
            if kwargs['pk']:
                """Удаляем данные из таблицы по id записи"""
                """Возвращаем объект model из фабрики с измененными параментрами URL"""
                """реверса в атрибуте after_del_template_redirect"""
                obj_model = obj.chosen_factory.model.del_model_id(kwargs)
        return HttpResponseRedirect(reverse(obj_model.after_del_template_redirect, kwargs=kwargs))
