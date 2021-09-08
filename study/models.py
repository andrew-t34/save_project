from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Level(models.Model):
    """Градация уровня обучения"""
    name = models.CharField(max_length=255, verbose_name="Уровень обучения",)

    class Meta:
        verbose_name_plural = "Уровени обучения"

    def __str__(self):
        return (self.name)

    @staticmethod
    def get_absolute_url():
        return reverse('studymain')


class Field(models.Model):
    """Градация области обучения"""
    level = models.ForeignKey(Level, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, verbose_name="Область обучения",)

    class Meta:
        verbose_name_plural = "Области обучения"

    def __str__(self):
        return (self.name)


class Program(models.Model):
    """Градация программ обучения"""
    field = models.ForeignKey(Field, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, verbose_name="Программа обучения")
    fullname = models.TextField(default='', verbose_name="Полное название")

    class Meta:
        verbose_name_plural = "Программы обучения",


    def __str__(self):
        return (self.name)


class Module(models.Model):
    """Градация программ обучения"""
    program = models.ForeignKey(Program, null=True, on_delete=models.SET_NULL, related_name='modules')
    number = models.IntegerField(default=0, verbose_name="Порядковый номер")
    name = models.CharField(max_length=255, verbose_name="Модуль обучения")

    class Meta:
        verbose_name_plural = "Модули обучения"
        ordering = ["number"]

    def __str__(self):
        return (self.name)


class Topic(models.Model):
    """Темы обучения"""
    program = models.ForeignKey(Program, null=True, on_delete=models.SET_NULL, verbose_name="Программа обучения", related_name='topics')
    module = models.ForeignKey(Module, null=True, on_delete=models.SET_NULL, verbose_name="Модуль обучения")
    topic_number = models.IntegerField(default=0, verbose_name="Порядковый номер")
    title = models.CharField(max_length=255, verbose_name="Заголовок",)
    picture = models.ImageField('Картинка', default='', blank=True)
    text = models.TextField(verbose_name="Содержание")
    release_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateField(auto_now=True, verbose_name="Дата обновления")
    num_stars = models.IntegerField(verbose_name="Рейтинг", null=True)

    class Meta:
        verbose_name_plural = "Темы обучения"
        ordering = ['topic_number']

    def __str__(self):
        return (self.title)
