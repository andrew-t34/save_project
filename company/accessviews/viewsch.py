from company.viewbase import CompanyBase


class MainCompanySch(CompanyBase):

    template = 'company/sch/maincompany.html'


class CreateUpdateControllerSch(CompanyBase):
    permission_list_of_factories = ['company', 'customer']


class MyCustomersCompanySch(CompanyBase):
    template = 'company/sch/customer_companies.html'
