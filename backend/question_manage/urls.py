# encoding=utf-8
from django.urls import path
from question_manage import views

urlpatterns = [
    # excel批量导入试题
    path("import_question_from_excel/", views.import_question_from_excel),

    # 获取题库列表
    path("question_database_list/", views.question_database_list),

    # 修改考试、题库对应
    path("update_exam_manage_question_db/<int:exam_id>/", views.update_exam_question),
]