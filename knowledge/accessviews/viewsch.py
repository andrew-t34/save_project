from study.viewbase import StudyBase


class MainStudySch(StudyBase):

    template = 'study/sch/mainstudy.html'


class CreateUpdateSectionsSch(StudyBase):

    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']
    # template = 'contract/common/first_contract_form.html'


class DeleteSectionSch(StudyBase):

    permission_list_of_factories = ['level',
                                    'field',
                                    'program',
                                    'module',
                                    'topic']
    # template = 'contract/common/first_contract_form.html'


class ProgramDetailSch(StudyBase):

    template = 'study/sch/program_detail_sch.html'


class CreateUpdateModuleSch(StudyBase):
    pass


class CreateUpdateTopicSch(StudyBase):
    pass
