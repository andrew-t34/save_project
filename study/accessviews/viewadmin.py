from study.viewbase import StudyBase


class MainStudyAdmin(StudyBase):

    template = 'study/admin/mainstudy.html'


class CreateUpdateControllerAdmin(StudyBase):

    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']


class ListUnitAdmin(StudyBase):
    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']



class ProgramDetailAdmin(StudyBase):
    template = 'study/admin/program_detail_admin.html'
