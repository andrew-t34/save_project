import django_tables2 as tables
from study.models import Question
from django_tables2.utils import A

import itertools

TEMPLATE_QUESTION_ACTION = '''
   <div class="btn-group">
       <a href="{% url 'cu_study'  record.program_id  'question' record.pk %}" 
       class="btn btn-warning btn-sm"><i class="fa fa-pencil"></i></a>
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

    answers = tables.LinkColumn(
        "list_unit",
        text="Ответы",
        kwargs={'program_id': A("program_id"), 'pk': A("pk"), 'factory': 'answer'},
        verbose_name="",
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
        sequence = ('row_number', 'program', 'module', 'topic', 'text', 'answers')
        exclude = ('id',)

    def render_row_number(self):
        return next(self.counter)
