import django_tables2 as tables
from contract.models import Contract, FixPrice

import itertools

TEMPLATE = '''
   <div class="btn-group">
       <a href="{% url 'detail_contract' record.pk %}" class="btn btn-warning btn-sm"><i class="fa fa-search"></i></a>
   </div>
'''


TEMPLATE_FIX_PRICE = '''
   <div class="btn-group">
       <a href="{% url 'create_update_contract' 'fix_price' record.pk %}" class="btn btn-warning btn-sm"><i class="fa fa-pencil"></i></a>
   </div>
'''


class ContractTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name="№ пп",
        orderable=False, attrs={
            "td": {
                "width": 50
            }})

    new_actions = tables.TemplateColumn(
        TEMPLATE,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {
                "width": 50
            }
    })

    date = tables.Column(attrs={
        "td": {
            "width": 200
        }
    })

    number = tables.Column(attrs={
        "td": {
            "width": 200
        }
    })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    class Meta:
        attrs = {"class": "table table-bordered"}
        # template_name = "tables/mytable.html"
        model = Contract
        sequence = ('row_number', 'seller', 'customer', 'number', 'date')
        exclude = ('id', 'destroy')

    def render_row_number(self):
        return next(self.counter)


class FixPriceTable(tables.Table):
    row_number = tables.Column(
        empty_values=(),
        verbose_name="№ пп",
        orderable=False, attrs={
            "td": {
                "width": 50
            }})

    new_actions = tables.TemplateColumn(
        TEMPLATE_FIX_PRICE,
        orderable=False,
        verbose_name="",
        attrs={
            "td": {
                "width": 50
            }})

    program = tables.Column()

    price = tables.Column()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = itertools.count(1)

    class Meta:
        attrs = {"class": "table table-condensed"}
        model = FixPrice
        sequence = ('row_number', 'program', 'price')
        exclude = ('id', 'company')

    def render_row_number(self):
        return next(self.counter)

