import django_tables2 as tables
from study.models import Question, Answer
from django_tables2.utils import A

import itertools

TEMPLATE_QUESTION_ACTION = '''
   <div class="btn-group">
       <a href="{% url 'cu_question'  record.program_id  'question' record.pk %}" 
       class="btn btn-warning btn-sm"><i class="fa fa-pencil"></i></a>
   </div>
'''

TEMPLATE_ANSWER_ACTION = '''
   <div class="btn-group">
       <a href="{% url 'cu_answer' record.program_id record.question_id 'answer' record.pk %}"
       class="btn btn-warning btn-sm"><i class="fa fa-pencil"></i></a>
   </div>
   <div class="btn-group">
       <a href="{% url 'del_answer' record.program_id record.question_id  'answer' record.pk 'delete' %}"
       class="btn btn-danger btn-sm" id="delete"><i class="fa fa-trash"></i></a>
   </div>
'''


class QuestionTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name="№ пп",
        orderable=False, attrs={
            "td": {
                "width": 50
            }})

    new_actions = tables.TemplateColumn(
        TEMPLATE_QUESTION_ACTION,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {
                "width": 50
            }
        }
    )

    num_answers = tables.LinkColumn(
        "list_answer",
        kwargs={
            'program_id': A("program_id"),
            'topic_id': A("topic_id"),
            'question_id': A("pk"),
            'factory': 'answer'},
        verbose_name="Ответов",
    )

    module = tables.Column(
        accessor='topic__module'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    class Meta:
        attrs = {"class": "table table-bordered"}
        model = Question
        sequence = ('row_number', 'program', 'module', 'topic', 'text', 'num_answers')
        exclude = ('id',)

    def render_row_number(self):
        return next(self.counter)


"""------------------AnswerTable------------------------"""


class AnswerTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name="№ пп",
        orderable=False, attrs={
            "td": {
                "width": 50
            }})

    new_actions = tables.TemplateColumn(
        TEMPLATE_ANSWER_ACTION,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {
                "width": 100
            }
        }
    )

    question = tables.Column(
        accessor='question__text',
        verbose_name="Вопрос",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    class Meta:
        attrs = {"class": "table table-bordered"}
        model = Answer
        sequence = ('row_number', 'program', 'question', 'text', 'correct')
        exclude = ('id',)

    def render_row_number(self):
        return next(self.counter)
