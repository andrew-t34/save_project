from django.urls import path
from . import views


"""oshc.su/knowledge/"""
urlpatterns = [
    path('program/<int:program_id>', views.ProgramQuestions.as_view(), name='program_questions'),
    path('program/<int:program_id>/module/<int:module_id>/<slug:form_name>', views.CreateUpdateFormQuestion.as_view(),
         name='cr_up_questions'),
    path('program/<int:program_id>/module/<int:module_id>/<slug:form_name>/<int:pk>', views.CreateUpdateFormQuestion.as_view(),
         name='cr_up_questions'),
    path('program/<int:program_id>/module/<int:module_id>/question/<int:question_id>/<slug:form_name>',
         views.CreateUpdateFormAnswer.as_view(), name='cr_up_answer'),
    path('program/<int:program_id>/module/<int:module_id>/question/<int:question_id>/<slug:form_name>/<int:pk>',
         views.CreateUpdateFormAnswer.as_view(), name='cr_up_answer'),
    path('program/<int:program_id>/module/<int:module_id>/question/<int:question_id>/<slug:form_name>/<int:pk>/del',
         views.DeleteData.as_view(), name='delete'),
    path('program/<int:program_id>/module/<int:module_id>/<slug:form_name>/<int:pk>/del', views.DeleteData.as_view(),
         name='delete'),
]
