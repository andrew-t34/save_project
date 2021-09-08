from contract.viewbase import ContractBase
from contract.models import Contract


class MainContractHse(ContractBase):

    template = 'contract/hse/list_contract.html'

    def getContracts(self, user_id):
        customer_id = self.company.getCompany(user_id)
        return Contract.objects.all().filter(customer_id=customer_id).select_related('customer', 'seller')


class CreateUpdateControllerHse(ContractBase):
    permission_list_of_factories = [
        'contract'
    ]
    template = 'contract/common/first_contract_form.html'
