from knowledge.accessviews.viewsch import *
from knowledge.accessviews.viewadmin import *


class KnowledgeConfigurator:

    @staticmethod
    def get_object_group(request, view_name=''):
        classes = ''
        group = request.session['group']['name']
        if group == 'admin':
            classes = {'ProgramQuestions': ProgramQuestionsAdmin,
                       'CreateUpdateForm': CreateUpdateFormAdmin,
                       'DeleteData': DeleteDataAdmin}
        elif group == 'hse':
            classes = {}
        elif group == 'sch':
            classes = {}
        return classes[view_name]()


