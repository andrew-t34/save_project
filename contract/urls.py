from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainContract.as_view(), name='contract_main'),
    path('form/<slug:factory>', views.CreateUpdateController.as_view(), name='create_update_contract'),
    path('update/<int:pk>', views.CreateUpdateController.as_view(), name='create_update_contract'),
    path('update/<slug:factory>/<int:pk>', views.CreateUpdateController.as_view(), name='create_update_contract'),
    path('update/<slug:factory>/<slug:company>/<int:pk>', views.CreateUpdateController.as_view(), name='create_update_contract'),
    path('detail/<int:pk>', views.DetailContract.as_view(), name='detail_contract'),
    path('list_price', views.ListPriceProgram.as_view(), name='list_price')
]