import django_filters
from .models import Question


class QuestionFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(QuestionFilter, self).__init__(*args, **kwargs)
        self.filters['topic__module'].label = "Модуль"

    class Meta:
        model = Question
        fields = ['topic__module', 'topic']



