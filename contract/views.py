from django.views.generic.base import View
from django.shortcuts import render
from system.mixins.permission import PermissionGroupMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .factory import Configurator
from .tables import ContractTable, FixPriceTable
from django_tables2 import RequestConfig


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
                """представлен в файле этой группы папки access_view"""
                obj.select_form_factory(kwargs["factory"])
        return obj


class MainContract(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        contracts = obj.getContracts(request.user.id)
        table = ContractTable(contracts)
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page", 1), per_page=2)
        return render(request, obj.template, {'contracts': contracts, 'table': table})


class CreateUpdateController(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        if 'pk' in kwargs:
            self.data_for_form = obj.chosen_form_factory.model.get_data(kwargs, request)
        form = obj.chosen_form_factory.form.get_form(self.data_for_form, request)
        return render(request, obj.chosen_form_factory.template_form, {
            'form': form,
            'kwargs': kwargs,
            'account_data': self.data_for_form,
            'company_id': request.session['company_id'],
        })

    def post(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        form = obj.chosen_form_factory.form.get_form(request.POST, request)
        if form.is_valid():
            if 'del' in kwargs:
                obj.chosen_form_factory.model.del_data(form.cleaned_data, request)
            else:
                obj.chosen_form_factory.model.make_save(form.cleaned_data, request)
            return HttpResponseRedirect(reverse(obj.chosen_form_factory.redirect_url))
        else:
            return render(request, obj.chosen_form_factory.template_form, {
                "form": form,
                'kwargs': kwargs})


class DetailContract(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        return render(request, obj.template, {
            'contract': obj.getContractById(kwargs['pk'])}
        )


class ListPriceProgram(PermissionGroupMixin, BaseController, View):
    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = self.get_obj(request, kwargs)
        return render(request, obj.template, {
            'table': FixPriceTable(obj.get_price(request)),
            'company_id': request.session['company_id']})
