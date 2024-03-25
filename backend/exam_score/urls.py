# encoding=utf-8
from django.urls import path
from exam_score import views

urlpatterns = [
    # 学生答卷客观题判分
    path("calculate_score/<int:exam_id>/", views.calculate_score),

    # 老师判分主观题 获取未判分主观题
    path("get_sub_without_score/<int:exam_id>/", views.get_sub_without_score),
    # 老师判分主观题 提交主观题判分结果
    path("submit_sub_score/", views.submit_sub_score),

    # 交卷验证身份证后六位
    path("check_idcard_tail/<str:id_card>/", views.check_idcard_tail),
]