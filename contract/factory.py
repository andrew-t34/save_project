from contract.accessviews.viewadmin import *
from contract.accessviews.viewhse import *
from contract.accessviews.viewsch import *


class Configurator:

    def __init__(self, class_name):
        self.__class_name = class_name

    def get_object_group(self, request, view_name=''):
        group = request.session['group']['name']
        if group == 'admin':
            classes = {'MainContract': MainContractAdmin}
        elif group == 'hse':
            classes = {'MainContract': MainContractHse,
                       'CreateUpdateController': CreateUpdateControllerHse}
        elif group == 'sch':
            classes = {'MainContract': MainContractSch,
                       'CreateUpdateController': CreateUpdateControllerSch,
                       'DetailContract': DetailContractSch,
                       'ListPriceProgram': ListPriceProgramSch}
        return classes[self.__class_name]()


