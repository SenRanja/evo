# encoding=utf-8
from django.contrib.auth.models import Group
from django.db import models
from question_manage.models import ExamQuestion


class ExamManage(models.Model):
    EXAM_TYPE_CHOICES = [
        # (codeanme, name) 即 ( 选项代码， 选项名称)，实际存入数据库的是 codeanme
        ('考试', '考试'),
        ('模拟', '模拟'),
        ('作业', '作业'),
    ]

    # null=True影响数据库层面，表示数据库中的相应字段可以存储 NULL 值
    # blank=True允许为空字符串，与数据库的 NULL 值无关
    exam_name = models.CharField(max_length=150,default='未命名', verbose_name='考试命名')
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES, verbose_name='考试类型')
    start_time = models.DateTimeField(verbose_name='开始考试时间')
    end_time = models.DateTimeField(verbose_name='结束考试时间')
    # save 方法自动计算 end_time - start_time的分钟数
    duration = models.IntegerField(verbose_name='考试时长', blank=True, null=True)
    # duration = models.IntegerField(verbose_name='考试时长（分钟）', help_text='自动计算分钟', blank=True, null=True,)
    # auto_now_add=True 当对象第一次被创建时，字段的值被设置为当前日期和时间。该字段的值在对象创建后就不再更新。通常用于记录对象的创建时间。
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='考试管理创建时间', blank=True, null=True,)
    # auto_now=True 每次对象被保存时，字段的值都会被更新为当前日期和时间。即使对象未更改其他字段，也会更新该字段。通常用于记录对象的最后修改时间。
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='考试管理最后一次修改时间', blank=True, null=True,)
    # max_score = models.IntegerField(verbose_name='满分值设置', blank=True, null=True,)
    max_score = models.DecimalField(verbose_name='满分值设置', max_digits=5, decimal_places=1, blank=True, null=True)
    # 如果归档，学生的考试列表对本次考试不可见
    is_archived = models.BooleanField(default=False, verbose_name='考试管理封存（考试完了，永不可动）', blank=True, null=True,)
    # 多选题 默认false，少选不得分； true则少选得一半的分
    multiple_half = models.BooleanField(default=False, verbose_name='多选题 默认false，少选不得分； true则少选得一半的分', blank=True, null=True,)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration = int(delta.total_seconds() / 60)  # 将时间差转换为分钟数
            # self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '考试管理'
        db_table = "exam_manage"

class ExamManageClass(models.Model):
    '''考试场次对应班级'''
    group_class = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='参加考试的班级')
    exam_manage_pk = models.ForeignKey(ExamManage, on_delete=models.CASCADE, verbose_name='考试管理的场次')

    class Meta:
        verbose_name = '考试场次对应班级'
        db_table = "exam_manage_group_class"

class ExamManage_QuestionDatabase(models.Model):
    '''考试场次对应题库选择和配置'''
    QUESTION_TYPE_CHOICES = [
        # (codeanme, name) 即 ( 选项代码， 选项名称)，实际存入数据库的是 codeanme
        ('判断', '判断'),
        ('单选', '单选'),
        ('多选', '多选'),
        ('填空', '填空'),
        ('简答', '简答'),
        ('论述', '论述'),
    ]
    # 简单、中等、困难
    DIFFICULTY_LEVEL_CHOICES = [
        # (codeanme, name) 即 ( 选项代码， 选项名称)，实际存入数据库的是 codeanme
        ('easy', '简单'),
        ('middle', '中等'),
        ('hard', '困难'),
    ]
    # 考试场次选择
    exam_manage = models.ForeignKey(ExamManage, on_delete=models.CASCADE, verbose_name='考试管理的场次', null=True, blank=True,)
    # 题库选择
    question_database = models.CharField(max_length=150, verbose_name='题库名称', null=True, blank=True, )
    # 题目类型
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, verbose_name='试题类型', null=True, blank=True,)
    # 难度类型
    difficulty_level = models.CharField(max_length=15, choices=DIFFICULTY_LEVEL_CHOICES, verbose_name='难易程度', null=True, blank=True, )
    # 题目数量
    question_num = models.IntegerField(verbose_name='题目数量', null=True, blank=True,)
    # 单个题目分值设置
    # single_question_score = models.IntegerField(verbose_name='单个题目分值设置', null=True, blank=True,)
    single_question_score = models.DecimalField(verbose_name='单个题目分值设置', max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = '考试场次对应题库选择和配置'
        db_table = "exam_manage_question_database"
