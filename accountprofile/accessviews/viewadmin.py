from company.viewbase import CompanyBase
from company.models import Company
from django.shortcuts import render


class MainCompanyAdmin(CompanyBase):

    template = 'company/admin/maincompany.html'

    def getCompany(self, **kwargs):
        return Company.objects.all()
