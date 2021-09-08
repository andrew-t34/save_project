from .models import Contract, FixPrice
import datetime
from django.db.models import Max
from .forms import *
from company.views import CompanyBase
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from study.models import *

# Create your views here.

"""###############################CreateContractFactory###############################"""


class CreateContractFactory:

    def __init__(self):
        self.template_form = 'contract/common/first_contract_form.html'
        self.form = CreateContractForm()
        self.model = CreateContractModel()
        self.redirect_url = 'contract_main'


class CreateContractForm:
    def __init__(self):
        self.now = datetime.datetime.now()

    def get_form(self, *args):
        if args[0]:
            form = FirstContractForm(args[0] or None)
        else:
            form = FirstContractForm(initial={'number': self.takeNewNumberContract(), 'date': self.now.today()})
        return form

    def takeNewNumberContract(self):
        number = Contract.objects.all().filter(date__year=self.now.year).aggregate(Max('number'))
        if number['number__max']:
            number['number__max'] += 1
        else:
            number['number__max'] = 1
        return number['number__max']


class CreateContractModel:
    def __init__(self):
        self.company = CompanyBase()

    def get_data(self, id_contract, request):
        obj = Contract.objects.all().filter(id=id_contract).values()
        return obj[0]

    def del_data(self, id_contract):
        obj = Contract.objects.all().filter(id=id_contract['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data, request):
        default = {'number': cleaned_data['number'], 'date': cleaned_data['date']}
        if all([('inn' in cleaned_data), ('name' in cleaned_data), ('propety_id' in cleaned_data)]):
            try:
                customer = self.company.getCompanyByInn(cleaned_data['inn'])
            except ObjectDoesNotExist:
                customer = self.company.makeCompanySearchByInnAndSave(cleaned_data)
            seller = self.company.getCompany(request.user)
            default.update({'seller': seller, 'customer': customer})
        obj, created = Contract.objects.update_or_create(
            id=cleaned_data['id'],
            defaults=default,
        )
        return obj, created


"""###############################FixPriceFactory###############################"""


class FixPriceFactory:
    def __init__(self):
        self.template_form = 'contract/common/fix_price_form.html'
        self.form = FixPriceForm()
        self.model = FixPriceModel()
        self.redirect_url = 'list_price'


class FixPriceForm:

    def get_form(self, *args):
        program_id_list = []
        for id_program in Program.objects.values('id'):
            program_id_list.append({'program_id': id_program['id']})
        PriceFormSet = formset_factory(FormFixPrice, extra=0)
        """кастылЬ"""
        if args[0]:
            if args[1].POST:
                form = PriceFormSet(args[0])
            else:
                data = args[0].values()
                form = PriceFormSet(initial=data)
        else:
            form = PriceFormSet(
                initial=program_id_list
                )
        return form


class FixPriceModel:

    def get_data(self, kwargs, request):
        program_cost = FixPrice.objects.all().filter(company_id=kwargs['pk'])
        return program_cost


    def make_save(self, cleaned_data, request):
        for data in cleaned_data:
            data.update({'company_id': request.session['company_id']})
            obj, created = FixPrice.objects.update_or_create(
                id=data['id'],
                defaults=data,
            )
        return created



"""###################################ContractPriceFactory###################################"""


class ContractPriceFactory:
    def __init__(self):
        self.template_form = 'contract/common/contract_price_form.html'
        self.form = ContractPriceForm()
        self.model = ContractPriceModel()
        self.redirect_url = 'not defined'


class ContractPriceForm:
    pass


class ContractPriceModel:
    pass


"""###################################ContractBase###################################"""


class ContractBase:
    dict_of_factories = dict(
        contract=CreateContractFactory,
        fix_price=FixPriceFactory,
        contract_price=ContractPriceFactory,
    )

    def __init__(self):
        self.chosen_form_factory = ''
        self.company = CompanyBase()

    def select_form_factory(self, index):
        if index in self.dict_of_factories:
            self.chosen_form_factory = self.dict_of_factories[index]()
        else:
            return None

    def getContracts(self, user_id):
        seller_id = self.company.getCompany(user_id)
        return Contract.objects.all().filter(seller_id=seller_id).select_related('customer', 'seller')

    def getContractById(self, pk):
        return Contract.objects.filter(id=pk).select_related(
            'seller',
            'customer',
            'seller__propety',
            'customer__propety')

    def get_price(self, request):
        return FixPrice.objects.all().filter(company_id=request.session['company_id']).select_related('program',
                                                                                                   'program__field')
