from django.db import models
from company.models import Company
from study.models import Program


class Contract(models.Model):
    seller = models.ForeignKey(Company, models.SET_NULL, null=True, verbose_name="Продавец", related_name="seller")
    customer = models.ForeignKey(Company, models.SET_NULL, null=True, verbose_name="Клиент", related_name="customer")
    number = models.IntegerField(verbose_name="Номер догвора")
    date = models.DateField(verbose_name="Дата заключения")
    destroy = models.SmallIntegerField(verbose_name="Разорванные", null=True, default=0)

    class Meta:
        verbose_name_plural = "Договоры"

    # def __str__(self):
    #     return self.number


class ContractFile(models.Model):
    contract = models.ForeignKey(Company, models.SET_NULL, null=True, verbose_name="Школа")
    url_contract = models.FileField(verbose_name="Договор")

    class Meta:
        verbose_name_plural = "Договоры"

    def __str__(self):
        return self.url_contract


class ContractType(models.Model):
    company = models.ForeignKey(Company, models.SET_NULL, null=True, verbose_name="Школа")
    name = models.CharField(max_length=100, verbose_name="Имя")
    short_name = models.CharField(max_length=100, verbose_name="Индекс к номеру договора")

    class Meta:
        verbose_name_plural = "Тип договора"

    def __str__(self):
        return self.name


class ContractPrice(models.Model):
    contract = models.ForeignKey(Contract, models.CASCADE, verbose_name='Контракт', related_name='contracts')
    programs = models.ForeignKey(Program, models.CASCADE, verbose_name='Программа', related_name='program')
    price = models.IntegerField(verbose_name='Стоимость')

    class Meta:
        verbose_name_plural = 'Цены договоров'

    def __str__(self):
        return self.contract


class FixPrice(models.Model):
    program = models.ForeignKey(Program, models.CASCADE, verbose_name='Программа', related_name='fix_program')
    company = models.ForeignKey(Company, models.SET_NULL, null=True, verbose_name="Школа")
    price = models.IntegerField(verbose_name='Стоимость')

    class Meta:
        verbose_name_plural = 'Базовые цены'

    def __str__(self):
        return "Программа: {0}, Стоимость: {1}".format(self.program, self.price)
