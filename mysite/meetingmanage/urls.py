from django.urls import path

from . import views

urlpatterns = [
    # ex: /meetingmanage/
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('gendata/', views.index, name='gendata'),

]
