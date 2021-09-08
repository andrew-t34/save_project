from contract.viewbase import ContractBase
from contract.models import Contract
from company.models import Company
from django.shortcuts import render


class MainContractAdmin(ContractBase):

    template = 'contract/admin/list_contract.html'

    def getContracts(self, *args):
        return Contract.objects.all()
