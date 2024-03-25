# encoding=utf-8
from django.urls import path
from user import views, view_test

urlpatterns = [
    # 注册、登录、登出
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # login auth 登录验证
    path("login_check/", views.login_check),

    # 改密
    path("updatepassword/", views.updatepassword),

    # 批量导入用户数据
    path("import_user_from_excel/", views.import_user_from_excel),

    # 前端接口获取信息
    path("get_info/", views.get_info, name="register"),

    # 改密码
    path("change_passwd/", views.change_passwd),

    # 组
    path("group_q/", views.group_query),
    path("group_add/", views.group_add),
    path("group_add_user/", views.group_add_user),
    # 组 添加某用户
    path("group_add_user_by_sid/<int:group_id>/<str:sid>/", views.group_add_user_by_sid),
    # 组 更新用户列表
    path("group_delete_user_by_data/<int:group_id>/", views.group_delete_user_by_data),


    # 测试 view函数均在 view_test
    path("group_add/<str:group_name>/", view_test.group_add),
    path("group_del/<str:group_name>/", view_test.group_delete),
    path("user_has_perm/", view_test.user_has_perm),
    path("add_video/<str:video_name>/", view_test.add_video),
    path("del_video/<str:video_name>/", view_test.del_video),
    path("grp_assign_module/", view_test.grp_assign_module),
]
