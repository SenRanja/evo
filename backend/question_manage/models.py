# encoding=utf-8

from django.db import models

# Create your models here.
from subject_manage.models import Subject


class ExamQuestion(models.Model):
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

    # 【试题本身】

    # null=True影响数据库层面，表示数据库中的相应字段可以存储 NULL 值
    # blank=True允许为空字符串，与数据库的 NULL 值无关
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, verbose_name='试题类型', null=True, blank=True,)
    reference_answer = models.TextField(verbose_name='参考答案', null=True, blank=True,)
    question_name = models.CharField(max_length=100, verbose_name='试题名称', null=True, blank=True,)
    question_text = models.TextField(verbose_name='试题问题', null=True, blank=True,)
    choice_text = models.TextField(verbose_name='选择题选项配置', null=True, blank=True, )

    # models.ImageField(upload_to='question_images/' 将图片存入目录下而非数据库
    # question_image = models.ImageField(upload_to='question_images/', null=True, blank=True, verbose_name='题目图片')

    # 试题图片存入数据库  在数据库中是longblob类型，通常最大存储4GB，但是性能不如将图片存入目录下而非数据库
    # DRF默认不会处理二进制字段（例如 models.BinaryField）的序列化。要在 DRF 中序列化二进制字段，你需要使用自定义的序列化器，如传入base64编码的字符串，但是推荐此处不使用drf。
    question_image_data = models.BinaryField(verbose_name='题目图片', null=True, blank=True,)

    # 【试题评价方面】

    difficulty_level = models.CharField(max_length=15, choices=DIFFICULTY_LEVEL_CHOICES, verbose_name='难易程度', null=True, blank=True,)
    description = models.TextField(blank=True, null=True, verbose_name='出题描述')
    # subject = models.CharField(max_length=150, verbose_name='学科', null=True, blank=True,)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='学科', null=True, blank=True, )
    question_database = models.CharField(max_length=150, verbose_name='题库名称', null=True, blank=True,)
    author = models.CharField(max_length=50, verbose_name='出题人', null=True, blank=True,)

    class Meta:
        verbose_name = '考试试题'
        db_table = "exam_question"