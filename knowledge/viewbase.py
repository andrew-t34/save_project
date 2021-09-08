from .forms import *
from .models import *
from study.viewbase import StudyBase
from django.http import Http404
from django.forms import formset_factory


"""----------------QuestionForm------------------"""


class QuestionFactory:

    def __init__(self):
        self.template_form = 'knowledge/common/form_question.html'
        self.form = QuestionFactoryForm()
        self.model = QuestionFactoryModel()


class QuestionFactoryForm:

    def get_form(self, *args):
        if args[0]:
            form = QuestionForm(args[0])
        else:
            form = QuestionForm(initial={'program_id': args[1]['program_id'],
                                         'module_id': args[1]['module_id'], })
        return form


class QuestionFactoryModel:


    def get_model_id(self, id_module):
        obj = Question.objects.all().filter(id=id_module).values()
        return obj[0]

    def del_model_id(self, id_module):
        obj = Question.objects.all().filter(id=id_module)
        if obj.delete():
            return True
        return False

    def make_save_model(self, cleaned_data):
        obj, created = Question.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'program_id': cleaned_data['program_id'],
                      'module_id': cleaned_data['module_id'],
                      'text': cleaned_data['text'],
                      'complexity': cleaned_data['complexity']},
        )
        return obj, created


"""---------------- AnswerForm------------------"""

class AnswerFactory:

    def __init__(self):
        self.template_form = 'knowledge/common/form_answer.html'
        self.form = AnswerFactoryForm()
        self.model = AnswerFactoryModel()


class AnswerFactoryForm:

    def get_form(self, *args):
        if args[0]:
            form = AnswerForm(args[0])
        else:
            form = AnswerForm(initial={'question_id': args[1]['question_id']})
        return form


class AnswerFactoryModel:

    def __init__(self):
        self.after_del_template_redirect = ''
        self.after_del_kwargs_redirect = ''


    def get_model_id(self, id_answer):
        print(id_answer)
        obj = Answer.objects.all().filter(id=id_answer).values()
        return obj[0]

    def del_model_id(self, kwargs):
        print(kwargs)
        obj = Answer.objects.all().filter(id=kwargs['pk'])
        if obj.delete():
            self.after_del_template_redirect = 'cr_up_answer'
            kwargs.pop('pk')
            return self
        return False

    def make_save_model(self, cleaned_data):
        obj, created = Answer.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'question_id': cleaned_data['question_id'],
                      'number': cleaned_data['number'],
                      'text': cleaned_data['text'],
                      'status': cleaned_data['status']},
        )
        return obj, created


class KnowledgeBase:

    dict_of_factories = dict(
        question=QuestionFactory,
        answer=AnswerFactory,
    )

    def __init__(self):
        self.chosen_factory = ''

    def select_form_factory(self, name_form):
        if name_form in self.dict_of_factories:
            self.chosen_factory = self.dict_of_factories[name_form]()
        else:
            return Http404

    def select_questions(self, data):
        obj_p_m = StudyBase.get_program_module_by_id(self, data['program_id'])
        questions = Question.objects.filter(program=obj_p_m['programs'])
        obj_p_m['questions'] = questions or None
        count = []
        datas = {}
        for modules in obj_p_m['modules']:
            datas[modules.id] = 0
            for question in questions:
                if modules.id == question.module_id:
                    count.append(question)
            if len(count) > 0:
                datas[modules.id] = len(count)
            count.clear()
        obj_p_m['count_questions'] = datas or None
        return obj_p_m

    def select_answers(self, data):
        answers = Answer.objects.filter(question_id=data) or False
        return answers

