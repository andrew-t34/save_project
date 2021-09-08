from study.viewbase import StudyBase
from study.models import *


class MainStudyListener(StudyBase):

    template = 'study/listener/mainstudy.html'

    def get_sections(self):
        """выбираем программы по которым работник проходит обучение"""
        """Необходимо применить кеш редис для запоминания допущенных к обучению программ."""
        self.dict_of_sections['programs'] = Program.objects.all() or None
        return self.dict_of_sections


class ProgramDetailListener(StudyBase):

    template = 'study/listener/program_detail_listener.html'
