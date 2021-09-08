from knowledge.viewbase import KnowledgeBase


class ProgramQuestionsAdmin(KnowledgeBase):

    template = 'knowledge/admin/program_questions.html'


class CreateUpdateFormAdmin(KnowledgeBase):

    perm_list_form_factories = ['question', 'answer']


class CreateUpdateFormQuestions(KnowledgeBase):

    perm_list_form_factories = ['question', 'answer']


class CreateUpdateFormAnswer(KnowledgeBase):

    perm_list_form_factories = ['question', 'answer']


class DeleteDataAdmin(KnowledgeBase):
    perm_list_form_factories = ['question', 'answer']