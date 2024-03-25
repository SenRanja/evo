# encoding=utf-8
from django.db import models
from exam_manage.models import ExamManage
from question_manage.models import ExamQuestion
from user.models import User

class ExamScoreResult(models.Model):
    '''学生考试答卷成绩'''
    # 学生
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学生', null=True, blank=True,)
    # 虽然设置了外键，但是此处冗余写一下学生的 name、stu_id 使得成绩表更为直观
    # 学生姓名
    name = models.CharField(verbose_name="姓名", max_length=30, null=True, blank=True,)
    # stu_id
    stu_id = models.CharField(verbose_name="学号", max_length=20, null=True, blank=True,)

    # 考试场次
    exam_manage = models.ForeignKey(ExamManage, on_delete=models.CASCADE, verbose_name='考试场次', null=True, blank=True,)
    # 客观题得分
    objective_score = models.IntegerField(verbose_name='客观题得分', null=True, blank=True,)
    # 主观题得分
    subjective_score = models.IntegerField(verbose_name='主观题得分', null=True, blank=True,)
    # 总分
    score = models.IntegerField(verbose_name='总分', null=True, blank=True, )
    # 是否终止提交客观题 flag, False是可以，True则封闭客观题重复计算提交。客观题计算分数完毕修改为True
    sub_block = models.BooleanField(default=False, verbose_name='终止提交客观题', null=True, blank=True, )

    class Meta:
        verbose_name = '学生考试答卷成绩'
        db_table = "exam_score_result"

# 学生考试主观题答卷记录与成绩 （非立即判分）
class ExamSubjectiveResult(models.Model):
    '''学生考试主观题答卷'''
    # 主观题 or 客观题
    SUB_OBJ_CHOICES = [
        # (codeanme, name) 即 ( 选项代码， 选项名称)，实际存入数据库的是 codeanme
        ('主观', '主观'),
        ('客观', '客观'),
    ]

    # 学生
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='学生', null=True, blank=True, )
    # 考试场次
    exam_manage = models.ForeignKey(ExamManage, on_delete=models.CASCADE, verbose_name='考试场次', null=True, blank=True, )
    # 主观题 or 客观题
    sub_obj = models.CharField(max_length=20, verbose_name='主客观', choices=SUB_OBJ_CHOICES, null=True, blank=True, )
    # 试题
    exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, verbose_name='主观题试题', null=True, blank=True, )
    # 学生答卷
    stu_answer = models.TextField(verbose_name="学生答卷", null=True, blank=True,)
    # 得分
    score = models.IntegerField(verbose_name='分数', null=True, blank=True, )
    # 是否评分完毕 flag
    sub_block = models.BooleanField(default=False, verbose_name='评分完毕', null=True, blank=True, )


    class Meta:
        verbose_name = '学生考试主观题答卷'
        db_table = "exam_result_record"