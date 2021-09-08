from company.accessviews.viewadmin import *
from company.accessviews.viewhse import *
from company.accessviews.viewsch import *


class Configurator:

    def __init__(self, class_name):
        self.__class_name = class_name


    def get_object_group(self, request):
        group = request.session['group']['name']
        if group == 'admin':
            classes = {'MainCompany': MainCompanyAdmin}
        elif group == 'hse':
            classes = {'MainCompany': MainCompanyHse,
                       'CreateUpdateController': CreateUpdateControllerHse,
                       'Division': DivisionHse,
                       'Position': PositionHse,
                       'DeleteController': DeleteControllerHse}
        elif group == 'sch':
            classes = {'MainCompany': MainCompanySch,
                       'CreateUpdateController': CreateUpdateControllerSch,
                       'MyCustomersCompany': MyCustomersCompanySch}
        return classes[self.__class_name]()


