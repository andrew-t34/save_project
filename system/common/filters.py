import django_filters
from accountprofile.models import AccountProfile


"""Using fo accountprofile list table"""


class AccountProfileFilter(django_filters.FilterSet):
    class Meta:
        model = AccountProfile
        fields = ['name', 'second', 'middle', 'education']