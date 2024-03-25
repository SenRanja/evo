# encoding=utf-8
from django.urls import path
from notice import views

urlpatterns = [

    # 公告列表
    path("notice_list/", views.notice_list),

    # 新增 (公告, 班级) 对应关系
    path("notice_class_add/", views.notice_class_add),

    # 删除 (公告, 班级) 对应关系
    path("notice_class_del/", views.notice_class_del),

    # disha test
    path("notice_class_del/", views.notice_class_del),
    path("notice_class_del/", views.notice_class_del),
    path("notice_class_del/", views.notice_class_del),
    path("notice_class_del/", views.notice_class_del),

]