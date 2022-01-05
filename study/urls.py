from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainStudy.as_view(), name='studymain'),


    # ------------------- detail_program url -------------------------
    path('program/<int:program_id>',
         views.ProgramDetail.as_view(), name='program_detail'),
    path('program/<int:program_id>/topic/<int:topic_id>',
         views.ProgramDetail.as_view(), name='program_detail'),

    # ------------------- create url -------------------------

    path('create/<slug:factory>',
         views.CreateUpdateController.as_view(), name='create_unit'),
    path('create/<int:program_id>/<slug:factory>',
         views.CreateUpdateController.as_view(), name='create_program_unit'),
    path('create/<int:program_id>/<int:module_id>/<slug:factory>',
         views.CreateUpdateController.as_view(), name='create_topic_unit'),

    # ------------------- update url -------------------------

    path('update/<slug:factory>/<int:pk>',
         views.CreateUpdateController.as_view(), name='update_unit'),
    path('update/<int:program_id>/<slug:factory>/<int:pk>',
         views.CreateUpdateController.as_view(), name='update_program_unit'),


    # ------------------- delete url -------------------------

    path('update/<slug:factory>/<int:pk>/<slug:delete>',
         views.CreateUpdateController.as_view(), name='delete_unit'),

    # ------------------- list_unit url -------------------------

    path('list_unit/<slug:factory>',
         views.ListUnit.as_view(), name='list_unit'),
    path('list_unit/<int:program_id>/<slug:factory>',
         views.ListUnit.as_view(), name='list_unit'),
    path('list_unit/<int:program_id>/question/<int:question_id>/<slug:factory>',
         views.ListUnit.as_view(), name='list_unit'),

    # ------------------- dal url -------------------------

    path('level_dal', views.LevelAutocomplete.as_view(), name='level-dal'),
    path('field_dal', views.FieldAutocomplete.as_view(), name='field-dal'),
    path('module_dal', views.ModuleAutocomplete.as_view(), name='module-dal'),
    path('topic_dal', views.TopicAutocomplete.as_view(), name='topic_dal'),
]
