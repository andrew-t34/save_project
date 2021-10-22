from django import forms
from study.models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from dal import autocomplete


class LevelForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())
    name = forms.CharField(
        max_length=200,
        label="Название уровня обучения",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class FieldForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    level_id = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        to_field_name="id",
        empty_label="Пусто",
        label="Уровень обучения",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
        )

    name = forms.CharField(
        max_length=200,
        label="ИНН",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class ProgramForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    field__level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        label=u"Уровень обучения",
        widget=autocomplete.ModelSelect2(
            url='level-dal',
            attrs={
                'class': 'form-control'
            })
    )

    field_id = forms.ModelChoiceField(
        queryset=Field.objects.all(),
        label=u"Область",
        widget=autocomplete.ModelSelect2(
            url='field-dal',
            forward=['level'],
            attrs={
                'class': 'form-control'
            }
        )
    )

    name = forms.CharField(
        max_length=200,
        label="Название программы",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    fullname = forms.CharField(
        max_length=1000,
        label="Полное название программы",
        widget=forms.Textarea(
            attrs={
                'style': 'width: 100%',
                'class': 'form-control',
                'placeholder': 'Название должно быть не длиннее 1000 символов'
            },
        )
    )


class ModuleForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    program_id = forms.IntegerField(label='program_id', required=False, widget=forms.HiddenInput())

    number = forms.IntegerField(
        label='Номер модуля',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    name = forms.CharField(
        max_length=255,
        label="Название модуля",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class TopicForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    program_id = forms.IntegerField(label='Программа обучения', widget=forms.HiddenInput())

    module_id = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label='Модуль обучения',
        widget=autocomplete.ModelSelect2(
            url='module-dal',
            forward=['program_id'],
            attrs={
                'data-placeholder': 'Укажите модуль',
                'style': "width: 100%",
            }
        )
    )

    topic_number = forms.IntegerField(
        label='Порядковый номер',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    title = forms.CharField(
        label='Название темы',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    picture = forms.ImageField(label='Тематическая картинка', required=False)

    text = forms.CharField(
        label='Содержание',
        widget=CKEditorUploadingWidget())


class QuestionForm(forms.Form):

    id = forms.IntegerField(label='id', required=False, widget=forms.HiddenInput())

    program_id = forms.IntegerField(label='Программа обучения', widget=forms.HiddenInput())

    module_id = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label='Модуль обучения',
        widget=autocomplete.ModelSelect2(
            url='module-dal',
            forward=['program_id'],
            attrs={
                'data-placeholder': 'Укажите модуль',
                'style': "width: 100%",
            }
        )
    )

    topic_id = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        label='Тема обучения',
        widget=autocomplete.ModelSelect2(
            url='topic_dal',
            forward=['module_id'],
            attrs={
                'data-placeholder': 'Укажите тему',
                'style': "width: 100%",
            }
        )
    )

    text = forms.CharField(
        max_length=1000,
        label="Название модуля",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )


class TableQuestionFilter(forms.Form):
    program_id = forms.IntegerField(label='Программа обучения', widget=forms.HiddenInput())

    module_id = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        label='Модуль обучения',
        required=True,
        widget=autocomplete.ModelSelect2(
            url='module-dal',
            forward=['program_id'],
            attrs={
                'data-placeholder': 'Укажите модуль',
                'style': "width: 100%",
            }
        )
    )

    topic_id = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        label='Тема обучения',
        required=True,
        widget=autocomplete.ModelSelect2(
            url='topic_dal',
            forward=['module_id'],
            attrs={
                'data-placeholder': 'Укажите тему',
                'style': "width: 100%",
            }
        )
    )

