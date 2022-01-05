from study.accessviews.viewsch import *
from study.accessviews.viewadmin import *
from study.accessviews.viewlistener import *


class Configurator:

    def __init__(self, class_name):
        self.__class_name = class_name

    def get_object_group(self, **kwargs):
        group = kwargs['request'].session['group']['name']
        if group == 'admin':
            classes = {'MainStudy': MainStudyAdmin,
                       'CreateUpdateController': CreateUpdateControllerAdmin,
                       'ProgramDetail': ProgramDetailAdmin,
                       'ListUnit': ListUnitAdmin}
        elif group == 'hse':
            pass
        elif group == 'sch':
            classes = {'MainStudy': MainStudySch,
                       'CreateUpdateController': CreateUpdateControllerSch,
                       'ProgramDetail': ProgramDetailSch,
                       'CreateUpdateModule': CreateUpdateModuleSch,
                       'CreateUpdateTopic': CreateUpdateTopicSch,
                       'ListUnit': ListUnitSch}
        elif group == 'lst':
            classes = {'MainStudy': MainStudyListener,
                       'ProgramDetail': ProgramDetailListener}
        return classes[self.__class_name](**kwargs)


