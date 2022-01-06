from .forms import *
from .models import *
from .tables import *
from django_tables2 import RequestConfig
from django.db.models import Q
from django.db.models import Count


class BaseList:

    def __init__(self, obj_group):
        self.obj_group = obj_group


class LevelFactory(BaseList):

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_level.html'
        self.redirect_url = obj_group.redirect_factory_url or 'list_unit'
        self.model = LevelFactoryModel(self.obj_group)
        self.form = LevelFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'factory': self.obj_group.data_url['factory']}

    @property
    def list(self):
        return LevelList(self.obj_group)


class LevelFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.obj_group.request.POST:
            form = LevelForm(self.model_obj.obj_group.request.POST or None)
        elif 'pk' in self.model_obj.obj_group.data_url:
            form = LevelForm(self.model_obj.get_data_form())
        else:
            form = LevelForm()
        return form


class LevelFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        obj = self.obj_group.level_data.filter(id=self.obj_group.data_url['pk']).values()
        return obj[0]

    def del_data(self):
        obj = Level.objects.all().filter(id=self.obj_group.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Level.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'name': cleaned_data['name']},
        )
        return obj, created


class LevelList(BaseList):

    @property
    def template_list(self):
        return self.obj_group.template_factory_list[self.obj_group.data_url['factory']]

    def get_list(self):
        return self.obj_group.level_data


"""_______________________FieldFactory___________________________"""


class FieldFactory:

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_field.html'
        self.redirect_url = obj_group.redirect_factory_url or 'list_unit'
        self.model = FieldFactoryModel(self.obj_group)
        self.form = FieldFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'factory': self.obj_group.data_url['factory']}

    @property
    def list(self):
        return ListField(self.obj_group)


class FieldFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.obj_group.request.POST:
            form = FieldForm(self.model_obj.obj_group.request.POST or None)
        elif 'pk' in self.model_obj.obj_group.data_url:
            form = FieldForm(self.model_obj.get_data_form())
        else:
            form = FieldForm()
        return form


class FieldFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        obj = self.obj_group.field_data.filter(id=self.obj_group.data_url['pk']).values()
        return obj[0]

    def del_data(self):
        obj = self.obj_group.field_data.filter(id=self.obj_group.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Field.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'level_id': cleaned_data['level_id'].id, 'name': cleaned_data['name']},
        )
        return obj, created


class ListField(BaseList):

    @property
    def template_list(self):
        return self.obj_group.template_factory_list[self.obj_group.data_url['factory']]

    def get_list(self):
        return self.obj_group.field_data.select_related('level')


"""____________________ProgramFactory______________________________"""


class ProgramFactory:

    """request, keys, obj_group"""
    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_program.html'
        self.redirect_url = obj_group.redirect_factory_url or 'list_unit'
        self.model = ProgramFactoryModel(self.obj_group)
        self.form = ProgramFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'factory': self.obj_group.data_url['factory']}

    @property
    def list(self):
        return ProgramList(self.obj_group)


class ProgramFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.obj_group.request.POST:
            form = ProgramForm(self.model_obj.obj_group.request.POST or None)
        elif 'pk' in self.model_obj.obj_group.data_url:
            form = ProgramForm(self.model_obj.get_data_form())
        else:
            form = ProgramForm()
        return form


class ProgramFactoryModel(BaseList):

    def get_data_form(self):
        obj = self.obj_group.program_data.filter(id=self.obj_group.data_url['pk']).\
            select_related('field__level').values(
            'id',
            'field_id',
            'field__level',
            'name',
            'fullname')
        return obj[0]

    def del_data(self):
        obj = self.obj_group.program_data.filter(id=self.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Program.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={
                'field_id': cleaned_data['field_id'].id,
                'name': cleaned_data['name'],
                'fullname': cleaned_data['fullname']},
        )
        return obj, created


class ProgramList(BaseList):

        @property
        def template_list(self):
            return self.obj_group.template_factory_list[self.obj_group.data_url['factory']]

        def get_list(self):
            return self.obj_group.program_data.select_related('field', 'field__level')


"""_______________________MODULE____________________________"""


class ModuleFactory:

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_module.html'
        self.redirect_url = self.obj_group.redirect_factory_url or 'list_unit'
        self.model = ModuleFactoryModel(self.obj_group)
        self.form = ModuleFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'program_id': self.obj_group.data_url['program_id'], 'factory': self.obj_group.data_url['factory']}

    @property
    def list(self):
        return ModuleList(self.obj_group)


class ModuleFactoryForm:

    def __init__(self, factory_model):
        self.factory_model = factory_model

    def get_form(self):
        if self.factory_model.obj_group.request.POST:
            form = ModuleForm(self.factory_model.obj_group.request.POST or None)
        elif 'pk' in self.factory_model.obj_group.data_url:
            form = ModuleForm(self.factory_model.get_data_form())
        else:
            form = ModuleForm(initial={
                'program_id': self.factory_model.obj_group.data_url['program_id']
            })
        return form


class ModuleFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        if 'pk' in self.obj_group.data_url:
            obj = self.obj_group.module_data.filter(id=self.obj_group.data_url['pk']).values()
            return obj[0]
        else:
            return {}

    def del_data(self, id_module):
        obj = self.obj_group.module_data.filter(id=self.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Module.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={
                'program_id': cleaned_data['program_id'],
                'number': cleaned_data['number'],
                'name': cleaned_data['name']},
        )
        return obj, created


class ModuleList(BaseList):

    def __init__(self, obj_group):
        self.obj_model = TopicList(obj_group)

    @property
    def template_list(self):
        return self.obj_model.template_list

    def get_list(self):
        return self.obj_model.get_list()


"""____________________________TOPIC____________________________"""


class TopicFactory:

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_topic.html'
        self.redirect_url = self.obj_group.redirect_factory_url or 'list_unit'
        self.model = TopicFactoryModel(self.obj_group)
        self.form = TopicFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'program_id': self.obj_group.data_url['program_id'], 'factory': 'topic'}

    @property
    def list(self):
        return TopicList(self.obj_group)


class TopicFactoryForm:

    def __init__(self, factory_model):
        self.factory_model = factory_model

    def get_form(self):
        if self.factory_model.obj_group.request.POST:
            form = TopicForm(self.factory_model.obj_group.request.POST or None)
        elif 'pk' in self.factory_model.obj_group.data_url:
            form = TopicForm(self.factory_model.get_data_form())
        else:
            form = TopicForm(initial={
                'program_id': self.factory_model.obj_group.data_url['program_id'],
                'module_id': self.factory_model.obj_group.data_url['module_id']
            })
        return form


class TopicFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        if 'pk' in self.obj_group.data_url:
            obj = self.obj_group.topic_data.filter(id=self.obj_group.data_url['pk']).values()
            return obj[0]
        else:
            return {}

    def del_data(self, id_module):
        obj = self.obj_group.topic_data.filter(id=id_module)
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Topic.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'program_id': cleaned_data['program_id'],
                      'module_id': cleaned_data['module_id'].id,
                      'topic_number': cleaned_data['topic_number'],
                      'title': cleaned_data['title'],
                      'picture': cleaned_data['picture'],
                      'text': cleaned_data['text']},
        )
        return obj, created


class TopicList(BaseList):

    @property
    def template_list(self):
        return self.obj_group.template_factory_list['topic']

    def get_list(self):
        module_list = self.obj_group.module_data.filter(program_id=self.obj_group.data_url['program_id'])
        topics = self.obj_group.topic_data.filter(
            program_id=self.obj_group.data_url['program_id']).select_related(
            'module', 'program').order_by(
            'module')
        # for module in topics:
        #     module_list.append(module.module)
        # module_list = list(set(module_list))
        return topics, module_list


"""____________________________Question____________________________"""


class QuestionFactory:

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_question.html'
        self.redirect_url = 'list_unit'
        self.model = QuestionFactoryModel(self.obj_group)
        self.form = QuestionFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return self.obj_group.data_url

    @property
    def list(self):
        return QuestionList(self.obj_group)


class QuestionFactoryForm:

    def __init__(self, factory_model):
        self.factory_model = factory_model

    def get_form(self):
        if self.factory_model.obj_group.request.POST:
            form = QuestionForm(self.factory_model.obj_group.request.POST or None)
        elif 'pk' in self.factory_model.obj_group.data_url:
            form = QuestionForm(self.factory_model.get_data_form())
        else:
            if 'module_id' in self.factory_model.obj_group.data_url and \
                    'topic_id' in self.factory_model.obj_group.data_url:
                form = QuestionForm(initial={
                    'program_id': self.factory_model.obj_group.data_url['program_id'],
                    'module_id': self.factory_model.obj_group.data_url['module_id'],
                    'topic_id': self.factory_model.obj_group.data_url['topic_id'],
                })
            else:
                form = QuestionForm(initial={
                    'program_id': self.factory_model.obj_group.data_url['program_id']
                })
        return form


class QuestionFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        if 'pk' in self.obj_group.data_url:
            obj = self.obj_group.question_data.filter(
                id=self.obj_group.data_url['pk']).select_related('topic__module').values(
                'id', 'program_id', 'topic_id', 'topic__module_id', 'text'
            )
            obj = obj[0]
            obj['module_id'] = obj.pop('topic__module_id')
            return obj
        else:
            return {}

    def del_data(self):
        obj = self.obj_group.question_data.filter(id=self.obj_group.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Question.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={
                'program_id': cleaned_data['program_id'],
                'topic_id': cleaned_data['topic_id'].id,
                'text': cleaned_data['text']},
        )
        return obj, created


class QuestionList(BaseList):

    @property
    def template_list(self):
        return self.obj_group.template_factory_list[self.obj_group.data_url['factory']]

    def get_list(self):
        table_list = QuestionTable(self.get_filter())
        RequestConfig(self.obj_group.request, paginate={"per_page": 2}).configure(table_list)
        return table_list

    def get_filter(self):
        if 'module_id' in self.obj_group.request.GET and \
                self.obj_group.request.GET['module_id'] != '' and \
                'topic_id' in self.obj_group.request.GET and \
                self.obj_model.obj_group.request.GET['topic_id'] != '':
            data = self.obj_group.question_data.select_related('topic__module', 'program').filter(
                Q(topic__module_id=self.obj_group.request.GET['module_id']),
                Q(topic_id=self.obj_group.request.GET['topic_id']),
                program=self.obj_group.data_url['program_id']
            ).annotate(num_answers=Count('questions'))
        else:
            data = self.obj_group.question_data.select_related('topic__module', 'program').filter(
                program_id=self.obj_group.data_url['program_id']).annotate(num_answers=Count('questions'))
        return data

    def get_filter_form(self):
        if 'module_id' in self.obj_group.request.GET:
            form = TableQuestionFilter(initial={
                'program_id': self.obj_group.data_url['program_id'],
                'module_id': self.obj_group.request.GET['module_id'],
                'topic_id': self.obj_group.request.GET['topic_id'],
            })
        else:
            form = TableQuestionFilter(initial={
                'program_id': self.obj_group.data_url['program_id']
            })
        return form


"""____________________________AnswerFactory____________________________"""


class AnswerFactory:

    def __init__(self, obj_group):
        self.obj_group = obj_group
        self.template_form = 'study/common/form_answer.html'
        self.redirect_url = 'list_unit'
        self.model = AnswerFactoryModel(self.obj_group)
        self.form = AnswerFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        if 'delete' in self.obj_group.data_url:
            self.obj_group.data_url.pop('delete')
            self.obj_group.data_url.pop('pk')
        return self.obj_group.data_url

    @property
    def list(self):
        return AnswerList(self.model)


class AnswerFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.obj_group.request.POST:
            form = AnswerForm(self.model_obj.obj_group.request.POST or None)
        elif 'pk' in self.model_obj.obj_group.data_url:
            form = AnswerForm(self.model_obj.get_data_form())
        else:
            form = AnswerForm(initial={
                'question_id': self.model_obj.obj_group.data_url['question_id'],
                'program_id': self.model_obj.obj_group.data_url['program_id']
            })
        return form


class AnswerFactoryModel:

    def __init__(self, obj_group):
        self.obj_group = obj_group

    def get_data_form(self):
        if 'pk' in self.obj_group.data_url:
            obj = self.obj_group.answer_data.filter(id=self.obj_group.data_url['pk']).select_related('question').values(
                'id', 'question_id', 'program_id', 'text', 'correct'
            )
            return obj[0]
        else:
            return {}

    def del_data(self):
        obj = self.obj_group.answer_data.filter(id=self.obj_group.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Answer.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={
                'program_id': cleaned_data['program_id'],
                'question_id': cleaned_data['question_id'],
                'text': cleaned_data['text'],
                'correct': cleaned_data['correct']},
        )
        return obj, created


class AnswerList:

    def __init__(self, model):
        self.obj_model = model

    @property
    def template_list(self):
        return self.obj_model.obj_group.template_factory_list[self.obj_model.obj_group.data_url['factory']]

    def get_list(self):
        table_list = AnswerTable(self.obj_model.obj_group.answer_data.select_related('question').filter(
                question_id=self.obj_model.obj_group.data_url['question_id']
            ))
        RequestConfig(self.obj_model.obj_group.request, paginate={"per_page": 10}).configure(table_list)
        return table_list


class StudyBase:
    dict_of_factories = dict(
        level=LevelFactory,
        field=FieldFactory,
        program=ProgramFactory,
        module=ModuleFactory,
        topic=TopicFactory,
        question=QuestionFactory,
        answer=AnswerFactory,
    )

    program_data = Program.objects.all()

    def __init__(self, **kwargs):
        self.level_data = Level.objects.all()
        self.field_data = Field.objects.all()
        self.program_data = Program.objects.all()
        self.topic_data = Topic.objects.all()
        self.module_data = Module.objects.all()
        self.question_data = Question.objects.all()
        self.answer_data = Answer.objects.all()

    """obj_group объект определенной группы, полученный через базовый контроллер"""
    """и включает в себя текущий объект класса по принципу наследования"""
    def select_form_factory(self, obj_group):
        if obj_group.data_url['factory'] in self.dict_of_factories:
            return self.dict_of_factories[obj_group.data_url['factory']](obj_group)
        else:
            return None

    def get_program_module_by_id(self, data):
        """Получаем значения программы и из кеша значения модулей без обращения к базе данных"""
        program = Program.objects.get(id=data) or None
        module = program.modules.all() or None
        data = {
            'programs': program,
            'modules': module
        }
        return data
