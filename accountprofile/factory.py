from accountprofile.accessviews.viewadmin import *
from accountprofile.accessviews.viewhse import *
from accountprofile.accessviews.viewsch import *


class Configurator:

    def __init__(self, class_name):
        self.__class_name = class_name

    def get_object_group(self, request):
        group = request.session['group']['name']
        if group == 'admin':
            classes = {}
        elif group == 'hse':
            classes = {'UserAccountProfile': UserAccountProfileHse,
                       'ListAccountProfile': ListAccountProfileHse,
                       'DetailAccountProfile': DetailAccountProfileHse,
                       'CreateUpdateController': CreateUpdateControllerHse,
                       'DeleteController': DeleteControllerHse}
        elif group == 'sch':
            classes = {}
        return classes[self.__class_name]()


