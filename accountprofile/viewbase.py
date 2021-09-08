from .forms import *
from django.contrib import messages
from .models import AccountProfile, Present, History
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image


# Create your views here.

class CreateAccountProfileFactory:

    def __init__(self):
        self.template_form = 'accountprofile/common/create_account_form.html'
        self.form = CreateAccountProfileForm()
        self.model = CreateAccountProfileModel()
        self.redirect_url = 'list_account_profile'


class CreateAccountProfileForm:

    def get_form(self, *args):
        if args[0]:
            form = CreateAccountForm(args[0] or None)
        else:
            form = CreateAccountForm()
        return form


class CreateAccountProfileModel:

    def get_data(self, id_position, request):
        obj = AccountProfile.objects.all().filter(id=id_position).values()
        return obj[0]

    def del_data(self, id_position):
        obj = AccountProfile.objects.all().filter(id=id_position['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, request, cleaned_data):
        obj, created = AccountProfile.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'name': cleaned_data['name'],
                      'second': cleaned_data['second'],
                      'middle': cleaned_data['middle'],
                      'education': cleaned_data['education'],
                      'birthday': cleaned_data['birthday'],
                      'snils': cleaned_data['snils'],
                      })
        if created:
            present = Present.objects.create(
                account_profile_id=obj.id,
                company_id=request.session['company_id'],
                division_id=cleaned_data['division_id'].id,
                position_id=cleaned_data['position_id'].id,
                event='Прием',
                active_event=1,
                date_event=cleaned_data['date_event'],
            )

            History.objects.create(
                account_profile_id=obj.id,
                company_id=request.session['company_id'],
                division=cleaned_data['division_id'].name,
                position=cleaned_data['position_id'].name,
                event='Прием',
                date_event=cleaned_data['date_event'],
                present_id=present.id
            )
            return True
        return False


"""-----------EditAccountProfileFactory-------------------"""


class EditAccountProfileFactory:

    def __init__(self):
        self.template_form = 'accountprofile/common/edit_account_form.html'
        self.form = EditAccountProfileForm()
        self.model = EditAccountProfileModel()
        self.redirect_url = 'list_account_profile'


class EditAccountProfileForm:

    def get_form(self, *args):
        form = EditAccountForm(args[0] or None)
        return form


class EditAccountProfileModel:

    def get_data(self, id_account, request):
        obj = AccountProfile.objects.all().filter(
            id=id_account,
            present__company=request.session['company_id'],
            present__active_event=1).values()
        return obj[0]

    def del_data(self, id_account):
        obj = AccountProfile.objects.all().filter(id=id_account['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, request, cleaned_data):
        obj, created = AccountProfile.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'name': cleaned_data['name'],
                      'second': cleaned_data['second'],
                      'middle': cleaned_data['middle'],
                      'education': cleaned_data['education'],
                      'birthday': cleaned_data['birthday'],
                      'snils': cleaned_data['snils'],
                      })
        return obj, created


"""--------------------Transfer Form Factory-------------------------"""


class TransferAccountProfileFactory:

    def __init__(self):
        self.template_form = 'accountprofile/common/transfer_account_form.html'
        self.form = TransferAccountProfileForm()
        self.model = TransferAccountProfileModel()
        self.redirect_url = 'list_account_profile'


class TransferAccountProfileForm:

    def get_form(self, *args):
        if args[0]:
            form = TransferAccountForm(args[0] or None)
        else:
            form = TransferAccountForm(initial={'account_profile_id': args[1]['account']})
        return form


class TransferAccountProfileModel:

    def get_data(self, id_transfer, request):
        obj = Present.objects.all().filter(id=id_transfer).values()
        return obj[0]

    def del_data(self, id_transfer):
        obj = Present.objects.all().filter(account_profile_id=id_transfer['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, request, cleaned_data):
        if cleaned_data['id'] is None:
            last_event = Present.objects.filter(account_profile_id=cleaned_data['account_profile_id']).order_by('-date_event')[:1]
            active_event = last_event[0]
            active_event.active_event = 0
            active_event.save(update_fields=['active_event'])

        obj, created = Present.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'account_profile_id': cleaned_data['account_profile_id'],
                      'company_id': request.session['company_id'],
                      'division_id': cleaned_data['division_id'].id,
                      'position_id': cleaned_data['position_id'].id,
                      'event': 'Перевод',
                      'active_event': 1,
                      'date_event': cleaned_data['date_event'],
                      })

        if created:
            History.objects.create(
                account_profile_id=obj.account_profile_id,
                company_id=request.session['company_id'],
                division=cleaned_data['division_id'].name,
                position=cleaned_data['position_id'].name,
                event='Перевод',
                date_event=cleaned_data['date_event'],
                present_id=obj.id
            )
            return True
        return False


"""-----------Fire Form Factory--------------"""


class FireAccountProfileFactory:

    def __init__(self):
        self.template_form = 'accountprofile/common/fire_account_form.html'
        self.form = FireAccountProfileForm()
        self.model = FireAccountProfileModel()
        self.redirect_url = 'list_account_profile'


class FireAccountProfileForm:

    def get_form(self, *args):
        if args[0]:
            form = FireAccountForm(args[0] or None)
        else:
            form = FireAccountForm()
        return form


class FireAccountProfileModel:

    def get_data(self, id_account, request):

        obj = AccountProfile.objects.all().filter(
            id=id_account,
            present__company=request.session['company_id'],
            present__active_event=1).values()
        return obj[0]

    def del_data(self, request, cleaned_data):
        obj = Present.objects.all().filter(account_profile_id=cleaned_data['id'], company_id=request.session['company_id'])
        for item in obj:
            item.delete()
        return True


"""-----------Foto Form Factory--------------"""


class PhotoProfileFactory:

    def __init__(self):
        self.template_form = 'accountprofile/common/photo_account_form.html'
        self.form = PhotoProfileForm()
        self.model = PhotoProfileModel()
        self.redirect_url = 'list_account_profile'


class PhotoProfileForm:

    def get_form(self, *args):
        if args[0]:
            form = PhotoForm(args[0], args[1])
        else:
            # form = AccountProfileForm(initial={'division_id': args[1]['division_id']})
            form = PhotoForm()
        return form


class PhotoProfileModel:

    def get_data(self, id_account):
        obj = AccountProfile.objects.all().filter(id=id_account).values()
        return obj[0]

    def del_data(self, id_position):
        obj = AccountProfile.objects.all().filter(id=id_position['id'])
        if obj.delete():
            return True
        return False

    def make_save(self, request, cleaned_data):
        account = AccountProfile.objects.get(id=cleaned_data['id'])
        fs = FileSystemStorage(settings.MEDIA_ROOT + '/account_photo/', '/account_photo/')
        name = fs.get_alternative_name('logo', '.jpg')
        x = cleaned_data['x']
        y = cleaned_data['y']
        w = cleaned_data['width']
        h = cleaned_data['height']
        image = Image.open(request.FILES['foto'])
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(settings.MEDIA_ROOT+fs.url(name), 'jpeg')
        if account.foto:
            fs.delete(settings.MEDIA_ROOT + str(account.foto))
        obj, created = AccountProfile.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'foto': fs.url(name)})
        return obj, created


"""--------------------AccountProfileBase-----------------------"""


class AccountProfileBase:

    dict_of_factories = dict(
        create_account=CreateAccountProfileFactory,
        edit_account=EditAccountProfileFactory,
        transfer_account=TransferAccountProfileFactory,
        fire_account=FireAccountProfileFactory,
        photo=PhotoProfileFactory,
    )

    def __init__(self):
        self.chosen_form_factory = ''

    def select_form_factory(self, index):
        if index in self.dict_of_factories:
            self.chosen_form_factory = self.dict_of_factories[index]()
        else:
            return None

    def get_account_profile_list(self, company_id):
        presents = Present.objects\
            .filter(company_id=company_id, active_event=1)\
            .select_related('account_profile', 'position', 'division')
        return presents

    def get_detail_account_profile(self, company_id, account_profile_id):
        account = Present.objects.filter(
            company_id=company_id,
            account_profile_id=account_profile_id,
            active_event=1)\
            .select_related('account_profile', 'position', 'division', 'company')
        return account

    def get_present(self, company_id, account_profile_id):
        present = Present.objects.filter(
            company_id=company_id,
            account_profile_id=account_profile_id).order_by('-date_event')\
            .select_related('account_profile', 'position', 'division', 'company')
        return present

    def get_history(self, account_profile_id):
        history = History.objects.filter(
            account_profile_id=account_profile_id,
            present_id=None).order_by('-date_event').select_related('company')
        return history

