from django.urls import path
from . import views

urlpatterns = [
    path('list',
         views.ListAccountProfile.as_view(),
         name='list_account_profile'),
    path('detail/<int:pk>',
         views.DetailAccountProfile.as_view(),
         name='detail_account_profile'),
    path('update/<slug:factory>',
         views.CreateUpdateController.as_view(),
         name='update_account'),
    path('update/<slug:factory>/<int:pk>',
         views.CreateUpdateController.as_view(),
         name='update_account'),
    path('update/<slug:factory>/<slug:del>',
         views.CreateUpdateController.as_view(),
         name='update_account'),
    path('update/<slug:factory>/<slug:new_transfer>/<int:account>',
         views.CreateUpdateController.as_view(),
         name='update_account'),
]
