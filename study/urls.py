from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainStudy.as_view(), name='studymain'),

    path('update/<slug:factory>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<slug:factory>/<int:pk>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<slug:factory>/<int:pk>/<slug:delete>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('program/<int:program_id>', views.ProgramDetail.as_view(), name='program_detail'),
    path('update/<int:program_id>/<slug:factory>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<int:program_id>/<slug:factory>/<int:pk>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<int:program_id>/question/<int:question_id>/<slug:factory>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<int:program_id>/question/<int:question_id>/<slug:factory>/<int:pk>', views.CreateUpdateController.as_view(), name='cu_study'),
    path('update/<int:program_id>/question/<int:question_id>/<slug:factory>/<int:pk>/<slug:delete>', views.CreateUpdateController.as_view(), name='cu_study'),

    path('list_unit/<slug:factory>', views.ListUnit.as_view(), name='list_unit'),
    path('list_unit/<int:program_id>/<slug:factory>', views.ListUnit.as_view(), name='list_unit'),
    path('list_unit/<int:program_id>/question/<int:question_id>/<slug:factory>', views.ListUnit.as_view(), name='list_unit'),

    path('level_dal', views.LevelAutocomplete.as_view(), name='level-dal'),
    path('field_dal', views.FieldAutocomplete.as_view(), name='field-dal'),
    path('module_dal', views.ModuleAutocomplete.as_view(), name='module-dal'),
    path('topic_dal', views.TopicAutocomplete.as_view(), name='topic_dal'),
]
