from .forms import CompanyForm, DivisionForm, PositionForm
from django.contrib import messages
from .models import Company, Division, Position
from contract.models import Contract
import mptt


# Create your views here.

class UserCompanyFactory:

    def __init__(self):
        self.template_form = 'company/common/company_form.html'
        self.form = CompanyFactoryForm()
        self.model = UserCompanyFactoryModel()


class CustomerCompanyFactory:

    def __init__(self):
        self.template_form = 'company/common/company_form.html'
        self.form = CompanyFactoryForm()
        self.model = CustomerCompanyFactoryModel()
        self.redirect_url = 'customers'


class DivisionFactory:

    def __init__(self):
        self.template_form = 'company/common/division_form.html'
        self.form = DivisionFactoryForm()
        self.model = DivisionFactoryModel()
        self.redirect_url = 'divisions'


class PositionFactory:

    def __init__(self):
        self.template_form = 'company/common/position_form.html'
        self.form = PositionFactoryForm()
        self.model = PositionFactoryModel()
        self.redirect_url = 'divisions'


class PositionFactoryForm:

    def get_form(self, *args):
        if args[0]:
            form = PositionForm(args[0] or None)
        else:
            form = PositionForm(initial={'division_id': args[1]['division_id']})
        return form


class PositionFactoryModel:

    def get_data(self, id_position):
        obj = Position.objects.all().filter(id=id_position).values()
        return obj[0]

    def del_data(self, id_position):
        obj = Position.objects.all().filter(id=id_position['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, request, cleaned_data):
        obj, created = Position.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'name': cleaned_data['name'],
                      'division': cleaned_data['division_id'],
                      'quantity': cleaned_data['quantity']})
        return obj, created

#     ---------------Division---------------


class DivisionFactoryForm:

    def get_form(self, *args):
        if args[0]:
            form = DivisionForm(args[0] or None)
        else:
            form = DivisionForm()
        return form


class DivisionFactoryModel:

    def get_data(self, id_division):
        obj = Division.objects.all().filter(id=id_division).values()
        return obj[0]

    def del_data(self, request):
        obj = Division.objects.all().filter(id=request.POST['id'],
                                            company_id=request.session['company_id'])
        tree_id = obj[0].tree_id
        if obj[0].is_root_node():
            children = obj[0].get_children()
            for i in range(children.count()):
                children[0].move_to(None)
        else:
            ancestors = obj[0].get_ancestors(ascending=True, include_self=False)
            children = obj[0].get_children()
            for i in range(children.count()):
                children[0].move_to(ancestors[0], position='first-child')
        obj[0].delete()
        Division.objects.partial_rebuild(tree_id)
        return True


    def make_save(self, request, cleaned_data):
        obj, created = Division.objects.update_or_create(
            id=cleaned_data['id'], company_id=request.session['company_id'],
            defaults={'name': cleaned_data['name'],
                      'parent': cleaned_data['parent_id']},)
        return obj, created


class CompanyFactoryForm:

    def get_form(self, *args):
        if args[0]:
            form = CompanyForm(args[0] or None)
        else:
            form = CompanyForm()
        return form


class CompanyFactoryModel:

    def get_data(self, id_company):
        obj = Company.objects.all().filter(id=id_company).values()

        return obj[0]

    def del_data(self, id_company):
        obj = Company.objects.all().filter(id=id_company)
        if obj.deleuser_company():
            return True
        return False


class UserCompanyFactoryModel(CompanyFactoryModel):

    def make_save(self, request, cleaned_data):
        obj, created = Company.objects.update_or_create(
            id=cleaned_data['id'], user=request.user,
            defaults={'propety': cleaned_data['propety_id'],
                      'user': request.user,
                      'name': cleaned_data['name'],
                      'ogrn': cleaned_data['ogrn'],
                      'inn': cleaned_data['inn'],
                      'telephon': cleaned_data['telephon'],
                      'url': cleaned_data['url'],
                      'text': cleaned_data['text']},)
        return obj, created


class CustomerCompanyFactoryModel(CompanyFactoryModel):

    def make_save(self, request, cleaned_data):
        obj, created = Company.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'propety': cleaned_data['propety_id'],
                      'name': cleaned_data['name'],
                      'ogrn': cleaned_data['ogrn'],
                      'inn': cleaned_data['inn'],
                      'telephon': cleaned_data['telephon'],
                      'url': cleaned_data['url'],
                      'text': cleaned_data['text']},)
        return obj, created


class CompanyBase:
    dict_of_sections = {'company': ''}
    dict_of_factories = dict(
        user_company=UserCompanyFactory,
        customer=CustomerCompanyFactory,
        division=DivisionFactory,
        position=PositionFactory,
    )

    def __init__(self):
        self.chosen_form_factory = ''

    def select_form_factory(self, index):
        if index in self.dict_of_factories:
            self.chosen_form_factory = self.dict_of_factories[index]()
        else:
            return None

    def getCompany(self, user_id):
        company = Company.objects.all().filter(user=user_id).select_related()
        if company:
            company = company[0]
        else:
            company = False
        return company

    def getCompanyByInn(self, inn):
        return Company.objects.get(inn=inn)

    def makeCompanySearchByInnAndSave(self, form):
        """Используем данный метод для сохранения компании
        при формировании контракта по частичным данным
        (См. contract/viewbase.py)"""
        obj, created = Company.objects.update_or_create(
            inn=form['inn'],
            defaults={'propety': form['propety_id'],  'name': form['name'], 'inn': form['inn']},
        )
        return obj

    def getMyClient(self, user_id):
        my_company = Company.objects.get(user=user_id)
        return Contract.objects.filter(seller_id=my_company.id).select_related('customer').select_related('customer__propety')

    def get_all_division(self, request: object) -> object:
        divisions = Division.objects.all().filter(company_id=request.session['company_id'])
        return divisions

    def select_positions_for_division(self, divisions):
        queryset = divisions.prefetch_related('positions')
        division_position = {}
        for division in queryset:
            position = [position for position in division.positions.all()]
            if position:
                division_position.update({division.id: position})
        return division_position


    def select_position_without_division(self):
        empty_position = Position.objects.filter(division_id__isnull=True)
        return empty_position



# class CompanyBase(View):
#
#     def get_logo_form(self, request, company=''):
#         if company:
#             form = LogoForm(company[0])
#         else:
#             form = LogoForm()
#         return render(request, 'company/common/logo_form.html', {'form': form, 'company': company})
#

#     def upload_logo(self, request):
#         form = LogoForm(request.POST, request.FILES)
#         fs = FileSystemStorage(settings.MEDIA_ROOT + '/company/logos/', '/company/logos/')
#         company = self.get_company_by_id_and_user_id(request.user, request.POST['id'])
#         if form.is_valid():
#             for itr_company in company:
#                 name = fs.get_alternative_name('logo', '.jpg')
#                 logo_name = fs.save(name, request.FILES['logo'])
#                 logo_url = fs.url(logo_name)
#                 if itr_company.logo:
#                     fs.delete(settings.MEDIA_ROOT + str(itr_company.logo))
#                 company.update(
#                     logo=logo_url,
#                 )
#         return render(request, 'company/common/logo_form.html', {"form": form, 'company': company})
#
#
# class Message():
#
#     options = {
#         'Company': {
#             'True': 'Организация добавлена успешно.',
#             'False': 'Данные по организации успешно перезаписаны',
#         }
#     }
#
#     def __init__(self, saveresult):
#         self.saveresult = saveresult
#
#     def showMassages(self, request):
#         text = self.options[self.saveresult[0]._meta.object_name][str(self.saveresult[1])]
#         messages.success(request, text)
#
#
#     def upload_logo(self, request):
#         form = LogoForm(request.POST, request.FILES)
#         fs = FileSystemStorage(settings.MEDIA_ROOT + '/company/logos/', '/company/logos/')
#         company = self.get_company_by_id_and_user_id(request.user, request.POST['id'])
#         if form.is_valid():
#             for itr_company in company:
#                 name = fs.get_alternative_name('logo', '.jpg')
#                 logo_name = fs.save(name, request.FILES['logo'])
#                 logo_url = fs.url(logo_name)
#                 if itr_company.logo:
#                     fs.delete(settings.MEDIA_ROOT + str(itr_company.logo))
#                 company.update(
#                     logo=logo_url,
#                 )
#         return render(request, 'company/common/logo_form.html', {"form": form, 'company': company})
