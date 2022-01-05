from study.viewbase import StudyBase


class MainStudyAdmin(StudyBase):

    template = 'study/admin/mainstudy.html'

    def get_data(self):
        """Получеаем данные из базового класса для отображения данных для администратора"""
        """данная функция вызывается в view.py MainStudy при рендиренге страницы"""
        return {
            'level_count': self.level_data.count(),
            'field_count': self.field_data.count(),
            'program_count': self.program_data.count(),
            'topic_count': self.topic_data.count()
        }


class CreateUpdateControllerAdmin(StudyBase):

    permission_factory_list = ['level', 'field', 'program',
                               'module', 'topic', 'question',
                               'answer']

    redirect_factory_url = ''

    def __init__(self, **kwargs):
        self.request = kwargs['request']
        self.data_url = kwargs['data_url']
        super().__init__()


class ListUnitAdmin(StudyBase):
    permission_factory_list = ['level', 'field', 'program',
                               'module', 'topic', 'question',
                               'answer']

    template_factory_list = dict(
        field='study/admin/list_field.html',
        program='study/admin/list_program.html',
        level='study/admin/list_level.html',
        topic='study/admin/list_topic.html',
        question='study/admin/list_question.html',
        answer='study/admin/list_answer.html',
    )

    redirect_factory_url = ''

    def __init__(self, **kwargs):
        self.request = kwargs['request']
        self.data_url = kwargs['data_url']
        super().__init__()

class ProgramDetailAdmin(StudyBase):

    template = 'study/admin/program_detail_admin.html'

    def __init__(self, **kwargs):
        self.request = kwargs['request']
        self.data_url = kwargs['data_url']
        super().__init__()


