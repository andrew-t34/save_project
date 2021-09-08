from django.db import models
from  company.models import Division, Position, Company
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class AccountProfile(models.Model):
    MIDDLE_EDUCATION = 'MD'
    SPECIAL_EDUCATION = 'SP'
    HIGHER_EDUCATION = 'HI'
    LEVEL_EDUCATION = [
        (MIDDLE_EDUCATION, 'Среднее образование'),
        (SPECIAL_EDUCATION, 'Среднеспециальное образование'),
        (HIGHER_EDUCATION, 'Высшее образование'),
    ]
    name = models.CharField(verbose_name='Имя', max_length=100)
    second = models.CharField(verbose_name='Фамилия', max_length=100)
    middle = models.CharField(verbose_name='Отчество', max_length=100)
    education = models.CharField(verbose_name='Образование', max_length=100, choices=LEVEL_EDUCATION,)
    birthday = models.DateField(verbose_name='День рождения', )
    snils = models.CharField(verbose_name='СНИЛС', max_length=100)
    create = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='Обнавлен', auto_now=True)
    foto = models.ImageField(verbose_name='Аватар', upload_to='account_photo')
    education_file = models.FileField(verbose_name='Документ об образовании', max_length=100)

    class Meta:
        verbose_name_plural = "Профиль"

    def __str__(self):
        return "{0} {1} {2}".format(self.second, self.name,  self.middle)


class Present(models.Model):

    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE, related_name='present')
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True, verbose_name='Компания')
    division = models.ForeignKey(Division, models.SET_NULL, blank=True, null=True, verbose_name='Подразделение')
    position = models.ForeignKey(Position, models.SET_NULL, blank=True, null=True, related_name='children', verbose_name='Должность')
    event = models.CharField(max_length=10, verbose_name='Событие', default=None)
    active_event = models.IntegerField(verbose_name='Активная позиция', default=0)
    date_event = models.DateField(verbose_name='Дата события',  default=None)

    class Meta:
        verbose_name_plural = "Форма собственности"
        indexes = [
            models.Index(fields=['company', 'account_profile'])
        ]

    def __str__(self):
        return (self.account_profile.name)


class History(models.Model):
    account_profile = models.ForeignKey(AccountProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True, verbose_name='Компания')
    division = models.CharField(verbose_name='Подразделение', max_length=255)
    position = models.CharField(verbose_name='Должность', max_length=255)
    event = models.CharField(max_length=10, verbose_name='Событие', default=None)
    date_event = models.DateField(verbose_name='Дата события', default=None)
    present = models.ForeignKey(Present, verbose_name='Подразделение', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "история"
        indexes = [
            models.Index(fields=['account_profile'])
        ]

    # def __str__(self):
    #     return (self.account_profile)