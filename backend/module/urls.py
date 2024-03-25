# encoding=utf-8
from django.urls import path
from module import views

urlpatterns = [

    # path("get_front_menu/", views.get_front_menu),
    # path("admin_statistics3/", views.test_3),
    # path("admin_statistics2/", views.test_4),

    path("import_menu_excel/", views.import_excel),

    # 前端模块API
    path("test/", views.test),

    # 获取角色列表
    path("get_roles_list/", views.get_roles_list),
]