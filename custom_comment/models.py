from django.db import models
from django_comments_xtd.models import XtdComment
from study.models import Topic, Program


class CustomComment(XtdComment):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic_comments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_comments')

    def save(self, *args, **kwargs):
        # self.user_name = self.user.name
        self.topic = Topic.objects.get(id=self.object_pk)
        self.program = Program.objects.get(id=self.topic.program_id)
        super(CustomComment, self).save(*args, **kwargs)
