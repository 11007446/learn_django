from django.urls import path

from . import views

urlpatterns = [
    # ex: /meetingmanage/
    path('', views.index, name='default'),
    path('index/', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('gendata/', views.gendata, name='gendata'),
    path('cleardata/', views.cleardata, name='cleardata'),
    path('importExcel/', views.importExcel, name='importExcel'),
    path('delmeeting/', views.delmeeting, name='delmeeting'),
    path('showmeeting/', views.showmeeting, name='showmeeting'),
    path('submitedit/', views.submitedit, name='submitedit'),
    

]
