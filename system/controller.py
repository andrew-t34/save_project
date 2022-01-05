
class BaseController:

    def __init__(self, **kwargs):
        self.configurator = kwargs['configurator'](kwargs['class_name'])

    def get_obj(self, request, kwargs=''):
        """request - это данные из request. Приходят из функции get класса (объекта)"""
        # obj = self.configurator.get_object_group(request=request, data_url=kwargs)
        obj_group = self.configurator.get_object_group(request=request, data_url=kwargs)
        """configurator - получаем из factory см. метод init"""
        if 'factory' in kwargs:
            """Проверяем есть ли метко для выбора фабрики. Передается через URL"""
            if kwargs['factory'] in obj_group.permission_factory_list:
                """permission_list_of_factories - перечень фабрик доступных для группы пользователей"""
                """представлен в файле этой группы папки access_view"""
                factory_obj = obj_group.select_form_factory(obj_group=obj_group)
                """создали и вернули объект конкретной фабрики в зависимости от названия в kwargs"""
                """сам метод select_form_factory находится в родительском классе полученного обекта obj"""
                return factory_obj
            """Если фабрики форм не запрашивается, возвращаем объект соответствуещей группы из factory.py"""
        return obj_group