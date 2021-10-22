from study.viewbase import StudyBase


class MainStudyAdmin(StudyBase):

    template = 'study/admin/mainstudy.html'


class CreateUpdateControllerAdmin(StudyBase):

    permission_factory_list = ['level',
                               'field',
                               'program',
                               'module',
                               'topic',
                               'question']

    redirect_factory_url = ''


class ListUnitAdmin(StudyBase):
    permission_factory_list = ['level', 'field', 'program',
                               'module', 'topic', 'question']

    template_factory_list = dict(
        field='study/admin/list_field.html',
        program='study/admin/list_program.html',
        level='study/admin/list_level.html',
        question='study/admin/list_question.html',
    )

    redirect_factory_url = ''


class ProgramDetailAdmin(StudyBase):
    template = 'study/admin/program_detail_admin.html'
