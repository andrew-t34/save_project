from .forms import *
from .models import *


class LevelFactory:

    def __init__(self, data=False):
        self.template_list = 'study/sch/list_level.html'
        self.template_form = 'study/common/form_level.html'
        self.redirect_url = 'list_unit'
        self.form = LevelFactoryForm()
        self.model = LevelFactoryModel()
        self.list = ListLevel()


class LevelFactoryForm:

    def get_form(self, *args):
        return LevelForm(args[0] or None)


class LevelFactoryModel:

    def get_data(self, kwargs, request):
        obj = Level.objects.all().filter(id=kwargs['pk']).values()
        return obj[0]

    def del_data(self, id_level, request):
        obj = Level.objects.all().filter(id=id_level)
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data, request):
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

    def __init__(self, data=False):
        self.template_list = 'study/sch/list_field.html'
        self.redirect_url = 'list_unit'
        self.template_form = 'study/common/form_field.html'
        self.form = FieldFactoryForm()
        self.model = FieldFactoryModel()
        self.list = ListField()


class FieldFactoryForm:

    def get_form(self, *args):
        form = FieldForm(args[0] or None)
        return form


class FieldFactoryModel:

    def get_data(self, *args):
        obj = Field.objects.all().filter(id=args[0]['pk']).values()
        return obj[0]

    def del_data(self, id_field, request):
        obj = Field.objects.all().filter(id=id_field)
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data, request):
        obj, created = Field.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'level': cleaned_data['level_id'], 'name': cleaned_data['name']},
        )
        return obj, created

class ListField:

    def get_list(self):
        return Field.objects.all().select_related('level')

"""____________________ProgramFactory______________________________"""


class ProgramFactory:

    def __init__(self, data=False):
        self.template_form = 'study/common/form_program.html'
        self.template_list = 'study/sch/list_program.html'
        self.redirect_url = 'list_unit'
        self.form = ProgramFactoryForm()
        self.model = ProgramFactoryModel()
        self.list = ListProgram()


class ProgramFactoryForm:

    def get_form(self, *args):
        if args[0] and not 'level' in args[0]:
            level = Field.objects.get(id=args[0]['field_id'])
            args[0].update(level=level.level_id)
        return ProgramForm(args[0] or None)


class ProgramFactoryModel:

    def get_data(self, kwargs, request):
        obj = Program.objects.all().filter(id=kwargs['pk']).values()
        return obj[0]

    def del_data(self, id_program, request):
        obj = Program.objects.all().filter(id=id_program)
        if obj.delete():
            return True
        return False

    def make_save(self, cleaned_data, request):
        obj, created = Program.objects.update_or_create(
            id=cleaned_data['id'],
            defaults={'field_id': cleaned_data['field_id'].id, 'name': cleaned_data['name'], 'fullname': cleaned_data['fullname']},
        )
        return obj, created

class ListProgram:

        def get_list(self):
            return Program.objects.all().select_related('field','field__level')


"""__________________________________________________"""


class ModuleFactory:

    def __init__(self, kwargs):
        self.template_form = 'study/common/form_module.html'
        self.model = ModuleFactoryModel(kwargs)
        self.form = ModuleFactoryForm(self.model)
        self.redirect_url = 'program_detail'
        self.kwargs_redirect = self.get_kwargs_redirect(kwargs['keys'])

    def get_kwargs_redirect(self, kwargs):
        return {'program_id': kwargs['program_id']}


class ModuleFactoryForm:

    def __init__(self, data):
        self.data_obj = data

    def get_form(self):
        if self.data_obj.request.POST:
            form = ModuleForm(self.data_obj.request.POST or None)
        elif 'pk' in self.data_obj.data_url:
            form = ModuleForm(self.data_obj.get_data_form())
        else:
            form = ModuleForm(initial={
                'program_id': self.data_obj.data_url['program_id']
            })
        return form


class ModuleFactoryModel:

    def __init__(self, data):
        self.data_url = data['keys']
        self.request = data['request']

    def get_data_form(self):
        if 'pk' in self.data_url:
            obj = Module.objects.all().filter(id=self.data_url['pk']).values()
            return obj[0]
        else:
            return {}

    def del_data(self, id_module):
        obj = Module.objects.all().filter(id=id_module)
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

"""__________________________________________________"""


class TopicFactory:

    def __init__(self, kwargs):
        self.template_form = 'study/common/form_topic.html'
        self.redirect_url = 'program_detail'
        self.model = TopicFactoryModel(kwargs)
        self.form = TopicFactoryForm(self.model)
        self.kwargs_redirect = self.get_kwargs_redirect(kwargs['keys'])

    def get_kwargs_redirect(self, kwargs):
        return {'program_id': kwargs['program_id']}

class TopicFactoryForm:

    def __init__(self, data):
        self.data_obj = data

    def get_form(self):
        if self.data_obj.request.POST:
            form =  form = TopicForm(self.data_obj.request.POST or None)
        elif 'pk' in self.data_obj.data_url:
            form =  form = TopicForm(self.data_obj.get_data_form())
        else:
            form =  form = TopicForm(initial={
                'program_id': self.data_obj.data_url['program_id']
            })
        return form

class TopicFactoryModel:

    def __init__(self, data):
        self.data_url = data['keys']
        self.request = data['request']

    def get_data_form(self):
        if 'pk' in self.data_url:
            obj = Topic.objects.all().filter(id=id_module).values()
            return obj[0]
        else:
            return {}

    def del_data(self, id_module):
        obj = Topic.objects.all().filter(id=id_module)
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


class StudyBase:
    dict_of_factories = dict(
        level=LevelFactory,
        field=FieldFactory,
        program=ProgramFactory,
        module=ModuleFactory,
        topic=TopicFactory,
    )

    def __init__(self):
        self.level_data = Level.objects.all()
        self.field_data = Field.objects.all()
        self.program_data = Program.objects.all()
        self.topic_data = Topic.objects.all()

    def select_form_factory(self, **kwargs):
        if kwargs['keys']['factory'] in self.dict_of_factories:
            return self.dict_of_factories[kwargs['keys']['factory']](kwargs)
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