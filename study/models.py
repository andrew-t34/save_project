from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Level(models.Model):
    """Градация уровня обучения"""
    name = models.CharField(
        max_length=255,
        verbose_name="Уровень обучения",)

    class Meta:
        verbose_name_plural = "Уровени обучения"

    def __str__(self):
        return self.name

    @staticmethod
    def get_absolute_url():
        return reverse('studymain')


class Field(models.Model):
    """Градация области обучения"""
    level = models.ForeignKey(
        Level,
        null=True,
        on_delete=models.SET_NULL,
        related_name='levels')

    name = models.CharField(
        max_length=255,
        verbose_name="Область обучения",)

    class Meta:
        verbose_name_plural = "Области обучения"

    def __str__(self):
        return self.name


class Program(models.Model):
    """Градация программ обучения"""
    field = models.ForeignKey(
        Field,
        null=True,
        on_delete=models.SET_NULL,
        related_name='fields')

    name = models.CharField(
        max_length=255,
        verbose_name="Программа обучения")

    fullname = models.TextField(
        default='',
        verbose_name="Полное название")

    class Meta:
        verbose_name_plural = "Программы обучения",

    def __str__(self):
        return self.name


class Module(models.Model):
    """Градация программ обучения"""

    program = models.ForeignKey(
        Program,
        null=True,
        on_delete=models.SET_NULL,
        related_name='modules')

    number = models.IntegerField(
        default=0,
        verbose_name="Порядковый номер")

    name = models.CharField(
        max_length=255,
        verbose_name="Модуль обучения")

    class Meta:
        verbose_name_plural = "Модули обучения"
        ordering = ["number"]

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Темы обучения"""
    program = models.ForeignKey(
        Program,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Программа обучения",
        related_name='programs')

    module = models.ForeignKey(
        Module,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Модуль обучения")

    topic_number = models.IntegerField(
        default=0,
        verbose_name="Порядковый номер")

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",)

    picture = models.ImageField(
        'Картинка',
        default='', blank=True)

    text = models.TextField(verbose_name="Содержание")

    release_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания")

    update_date = models.DateField(
        auto_now=True,
        verbose_name="Дата обновления")

    num_stars = models.IntegerField(
        verbose_name="Рейтинг",
        null=True)

    class Meta:
        verbose_name_plural = "Темы обучения"
        ordering = ['topic_number']

    def __str__(self):
        return self.title


class Question(models.Model):

    program = models.ForeignKey(
        Program,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Программа обучения",
        related_name='question_programs')

    topic = models.ForeignKey(
        Topic,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Тема обучения",
        related_name='question_topics')

    text = models.TextField(
        verbose_name="Текст вопроса")

    class Meta:
        verbose_name_plural = "Темы обучения"

    def __str__(self):
        return self.text


class Answer(models.Model):

    program = models.ForeignKey(
        Program,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Программа обучения",
        related_name='answer_programs')

    question = models.ForeignKey(
        Question,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Тестовый вопрос",
        related_name='questions')

    text = models.TextField(
        verbose_name="Текст ответа")

    correct = models.BooleanField(
        default=False,
        verbose_name='Статус ответа')

    class Meta:
        verbose_name_plural = "Ответы на вопросы"

    def __str__(self):
        return self.text
