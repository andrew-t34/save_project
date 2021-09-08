from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from mptt.models import MPTTModel, TreeForeignKey
import mptt
from django.urls import reverse
# Create your models here.

fs = FileSystemStorage(location='/media/company/logo')


class Typepropety(models.Model):
    # Вид собственности
    name_short = models.CharField(max_length=30, verbose_name="Программа обучения")
    name_long = models.CharField(max_length=100, verbose_name="Программа обучения")

    class Meta:
        verbose_name_plural = "Форма собственности"

    def __str__(self):
        return (self.name_long)


class Company(models.Model):
    # Данные по компаниям
    propety = models.ForeignKey(Typepropety, models.SET_NULL,
                                null=True,
                                verbose_name="Форма собственности",
                                related_name='propeties')
    user = models.ForeignKey(User, models.SET_NULL, db_index=True, related_name='type_id', blank=False, null=True,
                             verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Название компани")
    ogrn = models.CharField(max_length=15, verbose_name="ОГРН", default='')
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    telephon = models.CharField(max_length=50, default='', verbose_name="Номер телефона")
    url = models.URLField(max_length=50, verbose_name="Сайт компании", default='')
    date_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateField(auto_now=True, verbose_name="Дата изменения")
    logo = models.ImageField('Логотип компании', storage=fs, upload_to='company/logo/', null=True, blank=True)
    text = models.TextField(verbose_name="Текст дополнительный")
    activated = models.IntegerField(default=0, verbose_name="Активация")
    type_company = models.CharField(max_length=12, verbose_name="Тип организации")

    class Meta:
        verbose_name_plural = "Данные компании"

    def __str__(self):
        return (self.name)

    def get_company_by_id_user(self, id):
        self.objects.all().filter(user=id).select_related()


class Division(MPTTModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")
    name = models.CharField(max_length=100, verbose_name="Название подразделения")
    subsidiary = models.BooleanField(default=False, verbose_name="Статус")
    parent = TreeForeignKey('self', models.SET_NULL, blank=True, null=True, related_name='children')

    class Meta:
        verbose_name_plural = "Подразделения"


    class MPTTMeta:
        order_insertion_by = []
        parent_attr = 'parent'

    def __str__(self):
        return (self.name)

    def get_absolute_url(self):
        return reverse('divisions_detail', args=[str(self.id)])


mptt.register(Division, order_insertion_by=['name'])


class Position(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name="Компания")

    quantity = models.IntegerField(
        default=0,
        verbose_name="Активация")

    division = models.ForeignKey(
        Division,
        models.SET_NULL,
        blank=True, null=True,
        verbose_name="Должности",
        related_name='positions')

    class Meta:
        verbose_name_plural = "Должность"

    def __str__(self):
        return (self.name)

