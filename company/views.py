from django.views.generic.base import View
from company.factory import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from system.mixins.permission import PermissionGroupMixin

# Create your views here.


class CreateUpdateController(PermissionGroupMixin, View):

    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        self.data_for_form = False
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.get_obj(request, **kwargs)
        if 'pk' in kwargs:
            self.data_for_form = obj.chosen_form_factory.model.get_data(kwargs['pk'])
        form = obj.chosen_form_factory.form.get_form(self.data_for_form, kwargs)
        return render(request, obj.chosen_form_factory.template_form, {
            'form': form,
            'factory': kwargs['factory'],
            'kwargs': kwargs})

    def post(self, request, **kwargs):
        obj = self.get_obj(request, **kwargs)
        form = obj.chosen_form_factory.form.get_form(request.POST)
        if form.is_valid():
            obj.chosen_form_factory.model.make_save(request, form.cleaned_data)
            # message = Message(result)
            # message.showMassages(request)
            return HttpResponseRedirect(reverse(obj.chosen_form_factory.redirect_url))
        else:
            return render(request, obj.chosen_form_factory.template_form, {
                "form": form,
                'factory': kwargs['factory']})

    def get_obj(self, request, **kwargs):
        obj = self.configurator.get_object_group(request)
        if kwargs['factory'] in obj.permission_list_of_factories:
            obj.select_form_factory(kwargs['factory'])
        return obj


class DeleteController(CreateUpdateController):

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        super().__init__(*args, **kwargs)

    def post(self, request, **kwargs):
        obj = self.get_obj(request, **kwargs)
        obj.chosen_form_factory.model.del_data(request)
        return HttpResponseRedirect(reverse(obj.chosen_form_factory.redirect_url))


class MainCompany(PermissionGroupMixin, View):

    permission_required = ['sch', 'admin', 'hse']

    def __init__(self, *args, **kwargs):
        self.company = Configurator(self.__class__.__name__)
        super().__init__(**kwargs)

    def get(self, request):
        obj = self.company.get_object_group(request)
        company = obj.getCompany(request.user.id)
        return render(request, obj.template, {'company': company})


class MyCustomersCompany(PermissionGroupMixin, View):
    permission_required = ['sch', 'admin']

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        obj = self.configurator.get_object_group(request)
        return render(request, obj.template, {'companies': obj.getMyClient(request.user.id)})


class Division(PermissionGroupMixin, View):

    permission_required = ['admin', 'hse']

    def __init__(self, *args, **kwargs):
        self.configurator = Configurator(self.__class__.__name__)
        super().__init__(**kwargs)

    def get(self, request):
        obj = self.configurator.get_object_group(request)
        divisions = obj.get_all_division(request)
        positions = obj.select_positions_for_division(divisions)
        empty_positions = obj.select_position_without_division()
        return render(request, obj.template, {'divisions': divisions,
                                              'positions': positions,
                                              'empty_positions': empty_positions})
