from .forms import *
from .models import *
from .tables import *
from django_tables2 import RequestConfig
from .filters import QuestionFilter
from django.db.models import Q

class LevelFactory:

    def __init__(self, kwargs):
        self.template_list = 'study/sch/list_level.html'
        self.template_form = 'study/common/form_level.html'
        self.redirect_url = 'list_unit'
        self.model = LevelFactoryModel(kwargs)
        self.form = LevelFactoryForm(self.model)
        self.list = ListLevel()
        self.kwargs_redirect = self.get_kwargs_redirect(kwargs['keys'])

    def get_kwargs_redirect(self, kwargs):
        return {'factory': kwargs['factory']}


class LevelFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = LevelForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = LevelForm(self.model_obj.get_data_form())
        else:
            form = LevelForm()
        return form


class LevelFactoryModel:

    def __init__(self, kwargs):
        self.data_url = kwargs['keys']
        self.request = kwargs['request']

    def get_data_form(self):
        obj = Level.objects.all().filter(id=self.data_url['pk']).values()
        return obj[0]

    def del_data(self):
        obj = Level.objects.all().filter(id=self.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Level.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'name': cleaned_data['name']},
        )
        return obj, created


class ListLevel:

    def get_list(self):
        return Level.objects.all()


"""_______________________FieldFactory___________________________"""


class FieldFactory:

    def __init__(self, data):
        self.data = data
        self.template_form = 'study/common/form_field.html'
        self.redirect_url = self.data['obj_group'].redirect_factory_url or 'list_unit'
        self.model = FieldFactoryModel(self.data)
        self.form = FieldFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'factory': self.data['data_url']['factory']}

    @property
    def list(self):
        return ListField(self.model)


class FieldFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = FieldForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = FieldForm(self.model_obj.get_data_form())
        else:
            form = FieldForm()
        return form


class FieldFactoryModel:

    def __init__(self, data):
        self.data_url = data['data_url']
        self.request = data['request']
        self.obj_group = data['obj_group']

    def get_data_form(self):
        obj = self.obj_group.field_data.filter(id=self.data_url['pk']).values()
        return obj[0]

    def del_data(self):
        obj = self.obj_group.field_data.filter(id=self.data_url['pk'])
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data):
        obj, created = Field.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'level_id': cleaned_data['level_id'].id, 'name': cleaned_data['name']},
        )
        return obj, created


class ListField:
    def __init__(self, model):
        self.obj_model = model

    @property
    def template_list(self):
        return self.obj_model.obj_group.template_factory_list[self.obj_model.data_url['factory']]

    def get_list(self):
        return self.obj_model.obj_group.field_data.select_related('level')


"""____________________ProgramFactory______________________________"""


class ProgramFactory:

    """request, keys, obj_group"""
    def __init__(self, data):
        self.data = data
        self.template_form = 'study/common/form_program.html'
        self.redirect_url = self.data['obj_group'].redirect_factory_url or 'list_unit'
        self.model = ProgramFactoryModel(self.data)
        self.form = ProgramFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'factory': self.data['data_url']['factory']}

    @property
    def list(self):
        return ListProgram(self.model)


class ProgramFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = ProgramForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = ProgramForm(self.model_obj.get_data_form())
        else:
            form = ProgramForm()
        return form


class ProgramFactoryModel:

    def __init__(self, data):
        self.data_url = data['data_url']
        self.request = data['request']
        self.obj_group = data['obj_group']

    def get_data_form(self):
        obj = self.obj_group.program_data.filter(id=self.data_url['pk']).select_related('field__level').values(
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
            defaults={'field_id': cleaned_data['field_id'].id, 'name': cleaned_data['name'], 'fullname': cleaned_data['fullname']},
        )
        return obj, created


class ListProgram:

        def __init__(self, model):
            self.obj_model = model

        @property
        def template_list(self):
            return self.obj_model.obj_group.template_factory_list[self.obj_model.data_url['factory']]

        def get_list(self):
            return self.obj_model.obj_group.program_data.select_related('field', 'field__level')


"""__________________________________________________"""


class ModuleFactory:

    def __init__(self, data):
        self.data = data
        self.template_form = 'study/common/form_module.html'
        self.redirect_url = self.data['obj_group'].redirect_factory_url or 'program_detail'
        self.model = ModuleFactoryModel(self.data)
        self.form = ModuleFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'program_id': self.data['data_url']['program_id']}

    @property
    def list(self):
        return ModuleList(self.model)


class ModuleFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = ModuleForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = ModuleForm(self.model_obj.get_data_form())
        else:
            form = ModuleForm(initial={
                'program_id': self.model_obj.data_url['program_id']
            })
        return form


class ModuleFactoryModel:

    def __init__(self, data):
        self.data_url = data['data_url']
        self.request = data['request']
        self.obj_group = data['obj_group']

    def get_data_form(self):
        if 'pk' in self.data_url:
            obj = self.obj_group.module_data.filter(id=self.data_url['pk']).values()
            return obj[0]
        else:
            return {}

    def del_data(self, id_module):
        obj = self.obj_model.obj_group.module_data.filter(id=self.data_url['pk'])
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


class ModuleList:

    def __init__(self, model):
        self.obj_model = model

    @property
    def template_list(self):
        return self.obj_model.obj_group.template_factory_list[self.obj_model.data_url['factory']]

    def get_list(self):
        return self.obj_model.obj_group.module_data.select_related('program')


"""__________________________________________________"""


class TopicFactory:

    def __init__(self, data):
        self.data = data
        self.template_form = 'study/common/form_topic.html'
        self.redirect_url = self.data['obj_group'].redirect_factory_url or 'program_detail'
        self.model = TopicFactoryModel(self.data)
        self.form = TopicFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return {'program_id': self.data['data_url']['program_id']}

    @property
    def list(self):
        return ListProgram(self.model)


class TopicFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = TopicForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = TopicForm(self.model_obоj.get_data_form())
        else:
            form = TopicForm(initial={
                'program_id': self.model_obj.data_url['program_id']
            })
        return form


class TopicFactoryModel:

    def __init__(self, data):
        self.data_url = data['data_url']
        self.request = data['request']
        self.obj_group = data['obj_group']

    def get_data_form(self):
        if 'pk' in self.data_url:
            obj = self.obj_group.topic_data.ilter(id=self.data_url['pk']).values()
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


class QuestionFactory:

    def __init__(self, data):
        self.data = data
        self.template_form = 'study/common/form_question.html'
        self.redirect_url = 'list_unit'
        self.model = QuestionFactoryModel(self.data)
        self.form = QuestionFactoryForm(self.model)

    @property
    def kwargs_redirect(self):
        return self.data['data_url']

    @property
    def list(self):
        return QuestionList(self.model)


class QuestionFactoryForm:

    def __init__(self, model):
        self.model_obj = model

    def get_form(self):
        if self.model_obj.request.POST:
            form = QuestionForm(self.model_obj.request.POST or None)
        elif 'pk' in self.model_obj.data_url:
            form = QuestionForm(self.model_obj.get_data_form())
        else:
            form = QuestionForm(initial={
                'program_id': self.model_obj.data_url['program_id']
            })
        return form


class QuestionFactoryModel:

    def __init__(self, data):
        self.data_url = data['data_url']
        self.request = data['request']
        self.obj_group = data['obj_group']

    def get_data_form(self):
        if 'pk' in self.data_url:
            obj = self.obj_group.question_data.filter(id=self.data_url['pk']).select_related('topic__module').values(
                'id', 'program_id', 'topic_id', 'topic__module_id', 'text'
            )
            obj = obj[0]
            obj['module_id'] = obj.pop('topic__module_id')
            return obj
        else:
            return {}

    def del_data(self, id_question):
        obj = self.obj_group.question_data.filter(id=id_question)
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


class QuestionList:

    def __init__(self, model):
        self.obj_model = model

    @property
    def template_list(self):
        return self.obj_model.obj_group.template_factory_list[self.obj_model.data_url['factory']]

    def get_list(self):
        table_list = QuestionTable(self.get_filter())
        RequestConfig(self.obj_model.request, paginate={"per_page": 2}).configure(table_list)
        return table_list

    def get_filter(self):
        if 'module_id' in self.obj_model.request.GET and self.obj_model.request.GET['module_id'] != '' and 'topic_id' in self.obj_model.request.GET and self.obj_model.request.GET['topic_id'] != '':
            data = self.obj_model.obj_group.question_data.select_related('topic__module', 'program').filter(
                Q(topic__module_id=self.obj_model.request.GET['module_id']),
                Q(topic_id=self.obj_model.request.GET['topic_id']),
                program=self.obj_model.data_url['program_id']
            )
        else:
            data = self.obj_model.obj_group.question_data.select_related('topic__module', 'program').filter(
                program_id=self.obj_model.data_url['program_id'])
        # return QuestionFilter(self.obj_model.request.GET, data)
        return data

    def get_filter_form(self):
        if 'module_id' in self.obj_model.request.GET:
            form = TableQuestionFilter(initial={
                'program_id': self.obj_model.data_url['program_id'],
                'module_id': self.obj_model.request.GET['module_id'],
                'topic_id': self.obj_model.request.GET['topic_id'],
            })
        else:
            form = TableQuestionFilter(initial={
                'program_id': self.obj_model.data_url['program_id']
            })
        return form


class StudyBase:
    dict_of_factories = dict(
        level=LevelFactory,
        field=FieldFactory,
        program=ProgramFactory,
        module=ModuleFactory,
        topic=TopicFactory,
        question=QuestionFactory,
    )

    def __init__(self):
        self.level_data = Level.objects.all()
        self.field_data = Field.objects.all()
        self.program_data = Program.objects.all()
        self.topic_data = Topic.objects.all()
        self.module_data = Module.objects.all()
        self.question_data = Question.objects.all()

    def select_form_factory(self, **kwargs):
        if kwargs['data_url']['factory'] in self.dict_of_factories:
            return self.dict_of_factories[kwargs['data_url']['factory']](kwargs)
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