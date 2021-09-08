from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from company.forms import Division
from mptt.forms import TreeNodeChoiceField
from company.models import Position
from accountprofile.models import Present


class TransferAccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'id' in args:
            queryset = Present.objects.filter(id=args[0]['id']).values()
            self.data = {**queryset[0]}
            self.fields['date_event'].label = 'Дата перевода'

    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())

    account_profile_id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())

    date_event = forms.DateField(
        label='Дата приема',
        help_text='Укажите дату трудового договора',
        widget=DatePickerInput(
            format='%d.%m.%Y',
        )
    )

    division_id = TreeNodeChoiceField(
        help_text='Для получения должностей сначало выберите подразделение',
        queryset=Division.objects.all(),
        level_indicator='_____',
        label="Подразделение",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    # position_id = forms.ModelChoiceField(
    #     # queryset=Position.objects.all(),
    #     help_text='Обязательно укажите должность работника',
    #     label=u"Должность работника",
    #     # widget=s2forms.ModelSelect2Widget(
    #     #     empty_label='Empty',
    #     #     model=Position,
    #     #     max_results=10,
    #     #     search_fields=['name__icontains'],
    #     #     dependent_fields={'division_id': 'division_id'},
    #     #     attrs={
    #     #         'data-minimum-input-length': 0,
    #     #         # 'data-placeholder': '------',
    #     #         # 'style': 'width: 50%'},
    #     #         'class': 'form-control',
    #     #     }
    #     # )
    # )


class EditAccountForm(forms.Form):
    MIDDLE_EDUCATION = 'MD'
    SPECIAL_EDUCATION = 'SP'
    HIGHER_EDUCATION = 'HI'
    LEVEL_EDUCATION = [
        (MIDDLE_EDUCATION, 'Среднее образование'),
        (SPECIAL_EDUCATION, 'Среднеспециальное образование'),
        (HIGHER_EDUCATION, 'Высшее образование'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())

    name = forms.CharField(
        label='Имя',
        max_length=100,
        help_text='Введите имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )

    second = forms.CharField(
        label='Фамилия',
        max_length=100,
        help_text='Введите фамилию',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )

    middle = forms.CharField(
        label='Отчество',
        max_length=100,
        help_text='Введите отчество',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )

    education = forms.ChoiceField(
        choices=LEVEL_EDUCATION,
        label='Введите уровне образования',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            })
    )

    birthday = forms.DateField(
        label='День рождения',
        help_text='Введите дату рождения',
        widget=DatePickerInput(
            format='%d.%m.%Y',
        )
    )

    snils = forms.CharField(
        label='СНИЛС',
        max_length=100,
        help_text='Введите СНИЛС работника',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'snils'
            })
    )


class CreateAccountForm(EditAccountForm, TransferAccountForm):
    pass


class FireAccountForm(forms.Form):

    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())


class AccountFotoForm(forms.Form):
    foto = forms.ImageField(
        label='Фото сотрудника',
        help_text='Имя', )


class DiplomaFileForm(forms.Form):
    education_file = forms.FileField(
        label='Документ об образовании',
        max_length=100,
        help_text='Имя', )


class PhotoForm(forms.Form):
    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    foto = forms.ImageField(label='Фото сотрудника')
