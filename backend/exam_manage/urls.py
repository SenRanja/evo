# encoding=utf-8
from django.urls import path
from exam_manage import views

urlpatterns = [
    # 增加 考试 班级 对应
    path("add_class_exam_manage/", views.add_class_exam_manage),

    # 增加 考试 题库 对应
    path("add_question_database_exam_manage/", views.add_question_database_exam_manage),

    # 返回当前用户考试场次
    path("get_exam_manages/", views.get_exam_manages),

    # 检测用户是否经历过考试
    path("detect_examed/<int:exam_id>/", views.detect_examed),

    # 获取试卷
    path("get_exam_paper/<int:exam_id>/", views.get_exam_paper),

    # 获取试卷的word格式
    path("generate_exam_paper_word/<int:exam_id>/", views.generate_exam_paper_word),

    # 获取已提交的旧卷
    path("get_old_results/<int:exam_id>/", views.get_old_results),
]