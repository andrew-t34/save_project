from study.viewbase import StudyBase


class MainStudySch(StudyBase):

    template = 'study/sch/mainstudy.html'


class CreateUpdateControllerSch(StudyBase):

    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']


class ProgramDetailSch(StudyBase):

    template = 'study/sch/program_detail_sch.html'


class CreateUpdateModuleSch(StudyBase):
    pass


class CreateUpdateTopicSch(StudyBase):
    pass


class ListUnitSch(StudyBase):
    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']
