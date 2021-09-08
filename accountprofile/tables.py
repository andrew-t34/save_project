import django_tables2 as tables
from .models import AccountProfile, Present
import django_filters


import itertools

TEMPLATE = '''
    <a href="{% url 'detail_account_profile' record.account_profile_id %}" ><i class="fa fa-search"></i></a>
'''


class AccountProfileTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name="№ пп",
        orderable=False, attrs={
            "td": {
                "width": 50
            }
        })

    second = tables.Column(accessor='account_profile.second')

    name = tables.Column(accessor='account_profile.name')

    middle = tables.Column(accessor='account_profile.middle')

    snils = tables.Column(accessor='account_profile.snils')

    new_actions = tables.TemplateColumn(
        TEMPLATE,
        verbose_name="",
        orderable=False, attrs={
            "td": {
                "width": 50
            }
        })

    birthday = tables.Column(attrs={
        "td": {
            "width": 200
        }
    })

    create = tables.Column(attrs={
        "td": {
            "width": 200
        }
    })

    update = tables.Column(attrs={
        "td": {
            "width": 200
        }
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    class Meta:
        attrs = {"class": "table table-bordered", "id": "account-profile-table"}
        model = Present
        sequence = (
            'row_number',
            'second',
            'name',
            'middle',
            'snils',
            'division',
            'position',
        )
        exclude = ('id', 'birthday', 'create', 'update', 'event', 'account_profile', 'company', 'active_event')
        orderable = False
        empty_text = '-'

    def render_row_number(self):
        return next(self.counter)
