from django.urls import path
from . import views


urlpatterns = [
    # ex: /meetingmanage/
    path('', views.indexlayui, name='indexlayui'),
    path('indexlayui/', views.indexlayui, name='indexlayui'),
    path('indexnewquery/', views.indexnewquery, name='indexnewquery'),
    path('delcheckedmeetingdata', views.delcheckedmeetingdata, name='delcheckedmeetingdata'),
    path('importExcel/', views.importExcel, name='importExcel'),
    path('cleardata/', views.cleardata, name='cleardata'),
    path('submitedit/', views.submitedit, name='submitedit'),
    path('downloadsigninsheet/', views.downloadsigninsheet, name='downloadsigninsheet'),
    path('sendweekplan/', views.sendweekplan, name='sendweekplan')

    # path('index/', views.index, name='index'),
    # path('gendata/', views.gendata, name='gendata'),
    # path('cleardata/', views.cleardata, name='cleardata'),
    # path('delmeeting/', views.delmeeting, name='delmeeting'),
    # path('showmeeting/', views.showmeeting, name='showmeeting'),
    # path('submitedit/', views.submitedit, name='submitedit')

]
