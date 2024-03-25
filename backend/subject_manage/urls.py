# encoding=utf-8
from django.urls import path
from subject_manage import views

urlpatterns = [
    # admin使用此管理班级
    path("get_subject_list/", views.get_subject_list),
]
