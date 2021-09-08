from company.viewbase import CompanyBase
from django.shortcuts import render


class MainCompanyHse(CompanyBase):

    template = 'company/hse/maincompany.html'


class CreateUpdateControllerHse(CompanyBase):
    permission_list_of_factories = ['user_company', 'division', 'position']
    template = 'company/common/first_contract_form.html'


class DivisionHse(CompanyBase):
    permission_list_of_factories = []
    template = 'company/hse/divisions.html'


class DeleteControllerHse(CompanyBase):
    permission_list_of_factories = ['user_company', 'division', 'position']
    template = 'company/hse/divisions.html'

#
# class DivisionCreateUpdateHse(DivisionBase):
#     permission_list_of_factories = ['subsidiary']


class PositionHse(CompanyBase):
    permission_list_of_factories = []
    template = 'company/hse/divisions.html'
