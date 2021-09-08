from django.shortcuts import render
from django.views.generic.base import View
from accountprofile.factory import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from system.mixins.permission import PermissionGroupMixin
from .tables import AccountProfileTable
from django_tables2 import RequestConfig
from system.common.filters import AccountProfileFilter

# Create your views here.


class BaseController:
    _class_name = ''

    def __init__(self, *args, **kwargs):
        self.data_for_form = False
        if self._class_name:
            self.configurator = Configurator(self._class_name)
        super().__init__(*args, **kwargs)

    def get_obj(self, request_data, kwargs=''):
        """request_data - это данные из request. Приходят из функции get класса (объекта)"""
        obj = self.configurator.get_object_group(request_data)
        """configurator - получаем из factory см. метод init"""
        if 'factory' in kwargs:
            """Проверяем есть ли метко для выбора фабрики. Передается через URL"""
            if kwargs['factory'] in obj.permission_list_of_factories:
                """permission_list_of_factories - перечень фабрик доступных для группы пользователей"""
                """представлен в файле этой группы папки accessview"""
                obj.select_form_factory(kwargs['factory'])
        return obj


class UserAccountProfile(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        super().__init__(*args, **kwargs)


class ListAccountProfile(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_obj(request, **kwargs)
        account_profile = obj.get_account_profile_list(request.session['company_id'])
        table = AccountProfileTable(account_profile)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page", 1), per_page=20)
        return render(request, obj.template, {'table': table})


class DetailAccountProfile(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_obj(request, kwargs)
        return render(request, obj.template, {
            'profile': obj.get_detail_account_profile(request.session['company_id'], kwargs['pk']),
            'presents': obj.get_present(request.session['company_id'], kwargs['pk']),
            'histories': obj.get_history(kwargs['pk']),
        })


class CreateUpdateController(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        if 'pk' in kwargs:
            self.data_for_form = obj.chosen_form_factory.model.get_data(kwargs['pk'], request)
        form = obj.chosen_form_factory.form.get_form(self.data_for_form, kwargs)
        return render(request, obj.chosen_form_factory.template_form, {
            'form': form,
            'kwargs': kwargs,
            'account_data': self.data_for_form})

    def post(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        form = obj.chosen_form_factory.form.get_form(request.POST, request.FILES)
        if form.is_valid():
            if 'del' in kwargs:
                obj.chosen_form_factory.model.del_data(request, form.cleaned_data)
            else:
                obj.chosen_form_factory.model.make_save(request, form.cleaned_data)
            return HttpResponseRedirect(reverse(obj.chosen_form_factory.redirect_url))
        else:
            return render(request, obj.chosen_form_factory.template_form, {
                "form": form,
                'kwargs': kwargs})
