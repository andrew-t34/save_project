from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from company.forms import CompanyContractBase


class LiteContractForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    number = forms.CharField(
        max_length=10,
        label="Номер договора",
        error_messages={'required': 'Поле обязательное для заполнеия'},
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Только цифры',
                'class': 'form-control'
            }))

    date = forms.DateField(
        label="Дата договора",
        error_messages={'required': 'Поле обязательное для заполнеия'},
        required=True,
        widget=DatePickerInput(format='%d.%m.%Y')
    )


class ContractPriceForm(forms.Form):
    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())
    program = forms.IntegerField(widget=forms.HiddenInput())
    contract = forms.IntegerField(widget=forms.HiddenInput())
    price = forms.IntegerField(
        label="Цена",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Только цифры',
                'class': 'form-control'
            }),
        error_messages={'required': 'Поле обязательное для заполнеия'},
    )


class FormFixPrice(forms.Form):
    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())
    program_id = forms.IntegerField(label='id1', required=False, widget=forms.HiddenInput())
    price = forms.IntegerField(
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Только цифры',
                'class': 'form-control'
            }),
        error_messages={'required': 'Поле обязательное для заполнеия'},
    )


class FirstContractForm(CompanyContractBase, LiteContractForm):
    pass
