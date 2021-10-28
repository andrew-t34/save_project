from django import template
from study.models import Question
register = template.Library()


@register.simple_tag
def questions_get(active_topic=None):
    if active_topic:
        return Question.objects.filter(topic_id=active_topic.id)
    return False
