from accountprofile.viewbase import AccountProfileBase


class ListAccountProfileHse(AccountProfileBase):
    template = 'accountprofile/hse/listaccountprofile.html'


class DetailAccountProfileHse(AccountProfileBase):
    template = 'accountprofile/hse/detail_account_profile.html'


class CreateUpdateControllerHse(AccountProfileBase):
    permission_list_of_factories = [
        'create_account',
        'photo',
        'edit_account',
        'transfer_account',
        'fire_account',
    ]


class UserAccountProfileHse(AccountProfileBase):
    permission_list_of_factories = []
    template = 'company/hse/divisions.html'


class DeleteControllerHse(AccountProfileBase):
    permission_list_of_factories = ['user_company', 'division', 'position']
    template = 'company/hse/divisions.html'
