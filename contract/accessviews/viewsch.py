from contract.viewbase import ContractBase


class MainContractSch(ContractBase):
    template = 'contract/sch/list_contract.html'


class CreateUpdateControllerSch(ContractBase):
    template = 'contract/common/first_contract_form.html'
    permission_list_of_factories = [
        'contract',
        'fix_price',
        'contract_price',
    ]


class DetailContractSch(ContractBase):
    template = 'contract/sch/detail_contract.html'


class ListPriceProgramSch(ContractBase):
    template = 'contract/sch/list_price.html'

