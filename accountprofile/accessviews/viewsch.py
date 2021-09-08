from company.viewbase import CompanyBase
from django.shortcuts import render
# from company.forms import CompanyForm
# from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


class MainCompanySch(CompanyBase):

    template = 'company/sch/maincompany.html'


class CreateUpdateControllerSch(CompanyBase):
    permission_list_of_factories = ['company']
    template = 'company/common/first_contract_form.html'


class MyClientCompanySch(CompanyBase):

    template = 'company/sch/customer_companies.html'