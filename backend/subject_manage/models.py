# encoding=utf-8
from django.contrib.auth.models import Group
from django.db import models
from user.models import User


class Subject(models.Model):
    '''管理学科'''
    subject = models.CharField(max_length=200, verbose_name='学科名字', unique=True)
    # 弃用，不使用 django的默认 Group 作为管理组，使用 SubjectStaffGroup 管理
    # 创建学科时，需要默认新建个组，该组是学科的组（外键）
    # staff_group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='教师管理组', null=True, blank=True, )
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    description = models.TextField(verbose_name='描述', null=True, blank=True,)

    class Meta:
        verbose_name = '学科管理'
        db_table = "subjects"

class SubjectClass(models.Model):
    '''学科--班级 对应关系'''
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='班级', null=True, blank=True, )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='学科', null=True, blank=True, )

    class Meta:
        verbose_name = '学科--班级 对应关系'
        db_table = "subject_group"

class SubjectStaffGroup(models.Model):
    '''管理学科--教师'''
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='学科', null=True, blank=True, )
    # 创建学科时，需要默认新建个组，该组是学科的组（外键）
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='教师', null=True, blank=True, )

    class Meta:
        verbose_name = '教师对学科的管理'
        db_table = "subjects_staff"