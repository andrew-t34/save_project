from study.viewbase import StudyBase
from study.models import *


class MainStudyListener(StudyBase):

    template = 'study/listener/mainstudy.html'

    def __init__(self, *args, **kwargs):
        self.request = kwargs['request']
        self.data_url = kwargs['data_url']
        super(MainStudyListener, self).__init__(*args, **kwargs)

    def get_data(self):
        """выбираем программы по которым работник проходит обучение"""
        """Необходимо применить кеш редис для запоминания допущенных к обучению программ."""
        return {'programs': self.program_data}


class ProgramDetailListener(StudyBase):

    template = 'study/listener/program_detail_listener.html'

    def __init__(self, *args, **kwargs):
        self.request = kwargs['request']
        self.data_url = kwargs['data_url']
        super(ProgramDetailListener, self).__init__(*args, **kwargs)
