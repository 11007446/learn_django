from django.urls import path

from . import views

urlpatterns = [
    # ex: /meetingmanage/
    path('', views.index, name='index'),
    path('gendata/', views.index, name='gendata'),
]
