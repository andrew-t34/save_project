from django import forms
from django.core import validators
# from django.core.files.uploadedfile import SimpleUploadedFile
import re
from django.core.exceptions import ValidationError
from .models import Typepropety, Division
from mptt.forms import TreeNodeChoiceField


def clean_telephon(value):
    match = re.fullmatch(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', value)
    if not match:
        raise forms.ValidationError("Формат номера должен быть 8(111)222-33-44")
    return value


def clean_ogrn(value):
    match = re.fullmatch(r'(\d{15})', value)
    if not match:
        raise forms.ValidationError("Вы должны ввести число из 15 цифр")
    return value


def clean_inn(value):
    match = re.fullmatch(r'(\d{10})', value)
    if not match:
        raise forms.ValidationError("Вы должны ввести число из 10 цифр")
    return value


def file_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Файл слишком большой. размер должен быть не более 2 MiB.')


class CompanyContractBase(forms.Form):

    """Базовый класс для наследования формы для компани и заключения контракта( ContractApp и CompanyApp формы)"""
    propety_id = forms.ModelChoiceField(
        queryset=Typepropety.objects.all(),
        to_field_name="id",
        empty_label="Пусто",
        label="Форма собственности",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))

    inn = forms.CharField(
        max_length=10,
        label="ИНН",
        validators=[clean_inn],
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '773452345674',
                'class': 'form-control'
            }))

    name = forms.CharField(
        max_length=100,
        label="Название компани",
        error_messages={'required': 'Поле обязательное для заполнеия'},
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Рога и копыта',
                'class': 'form-control'
            }))


class CompanyForm(CompanyContractBase):
    # id = forms.IntegerField(widget=forms.HiddenInput(), label='')
    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    ogrn = forms.CharField(
        max_length=15,
        label="ОГРН",
        required=True,
        help_text='Число из 15 знаков',
        validators=[clean_ogrn],
        widget=forms.TextInput(
            attrs={
                'placeholder': '773452345674',
                'class': 'form-control'
            }))

    telephon = forms.CharField(
        max_length=50,
        label="Номер телефона",
        validators=[clean_telephon],
        required=True,
        help_text='Телефон компании',
        widget=forms.TextInput(
            attrs={
                'placeholder': '+79160146441',
                'class': 'form-control'
            }))

    url = forms.CharField(
        label="Адрес сайта",
        help_text='Корпоративный сайт компании',
        validators=[validators.URLValidator()],
        initial='http://',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
            }))

    text = forms.CharField(
        label="Дополнительная информация",
        required=False,
        validators=[validators.MaxLengthValidator(500)],
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Допускается объем текста не более 500 символов',
                'class': 'form-control',
                'rows': 3,
            }))


class LogoForm(forms.Form):
    # id = forms.IntegerField(widget=forms.HiddenInput(), label='')
    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())

    logo = forms.ImageField(
        label="Логотип компании",
        required=True,
        validators=[file_size], )


class DivisionForm(forms.Form):
    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput())

    name = forms.CharField(
        label='Название подразделения',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )

    subsidiary = forms.BooleanField(
        required=False,
        label='Является обособкой',
        widget=forms.CheckboxInput(

        )
    )

    parent_id = TreeNodeChoiceField(
        required=False,
        queryset=Division.objects.all(),
        level_indicator='_____',
        label="Родительское подразделение",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )


class PositionForm(forms.Form):

    id = forms.IntegerField(
        label='id',
        required=False,
        widget=forms.HiddenInput()
    )

    division_id = TreeNodeChoiceField(
        queryset=Division.objects.all(),
        level_indicator='--->',
        label="Подразделение",
        help_text='Определить для должности подразделение',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'multiple': '',
                'size': 15
            }
        )
    )

    name = forms.CharField(
        max_length=50,
        label='Название должности',
        help_text='Укажите должность, желательно в соответствии ОК-16',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )

    quantity = forms.IntegerField(
        label='Количество штатных единиц',
        help_text='Введите количество штатных диниц',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )
