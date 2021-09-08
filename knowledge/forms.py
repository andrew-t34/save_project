from django import forms


class QuestionForm(forms.Form):
    COEFFICIENT_CHOICES = [
        ('', '-----------'),
        (1.0, 'Легкий'),
        (1.25, 'Средний'),
        (1.5, 'Тяжелый'),
        (1.75, 'Неимоверный'),
    ]

    id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    program_id = forms.IntegerField(widget=forms.HiddenInput)

    module_id = forms.IntegerField(widget=forms.HiddenInput)

    topic_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    text = forms.CharField(label='Текст вопроса',
                           help_text="Не более 500 символов",
                           max_length=500,
                           min_length=30,
                           error_messages={'required': 'Пожалуйста введите текст вопроса'},
                           widget=forms.TextInput(
                               attrs={'size': '100%'}
                           ))

    complexity = forms.ChoiceField(label='Сложность вопроса',
                                   help_text="Сложность вопроса влияет на количество баллов",
                                   choices=COEFFICIENT_CHOICES, widget=forms.Select(),
                                   )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'


class AnswerForm(forms.Form):

    id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    question_id = forms.IntegerField(widget=forms.HiddenInput)

    number = forms.IntegerField(label="Номер",
                                help_text="Обязательно ввести номер вопроса",
                                widget=forms.NumberInput(
                                    attrs={
                                        'class': 'form-control'
                                    }
                                ))

    text = forms.CharField(label='Текст ответа',
                           help_text="Не более 500 символов",
                           max_length=500,
                           min_length=5,
                           error_messages={'required': 'Пожалуйста введите текст вопроса'},
                           widget=forms.Textarea(
                               attrs={'class': 'form-control',
                                      'rows': '3'}
                           ))

    status = forms.BooleanField(label='Отметить правильный ответ', required=False)
