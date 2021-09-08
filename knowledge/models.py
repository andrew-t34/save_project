from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Complexity(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Уровень сложности"


class Question(models.Model):

    program = models.ForeignKey('study.Program', on_delete=models.SET_NULL, blank=True, null=True)
    module = models.ForeignKey('study.Module', on_delete=models.SET_NULL, blank=True, null=True)
    topic = models.ForeignKey('study.Topic', on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(max_length=500)
    complexity = models.FloatField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = "Вопросы тестирования"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    text = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Ответы к вопросам"

    def __str__(self):
        return self.text

    ordering = ["number"]


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    # worker = models.ForeignKey('Worker', on_delete=models.DO_NOTHING) """не создан в Worker"""
    program = models.ForeignKey('study.Program', on_delete=models.PROTECT)
    # order = models.ForeignKey('contract.Order', null=True, blank=True) """не создан в Contract"""
    result = models.BooleanField()
    detail_result = models.CharField(max_length=500)
    score = models.IntegerField()
    wrong = models.IntegerField()
    right = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Тестирование от {} с результатом {} от пользователя {}'.format(self.date, self.result, self.user)

    class Meta:
        verbose_name_plural = "Результаты тестирования"
