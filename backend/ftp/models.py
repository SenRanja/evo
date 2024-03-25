# encoding=utf-8

from django.db import models
from user.models import User
from subject_manage.models import Subject


class Ftp(models.Model):
    '''资料'''
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='学科', null=True, blank=True, )
    # subject = models.CharField(verbose_name="学科", max_length=300, null=True, blank=True,)
    title = models.CharField(verbose_name="资料标题", max_length=300, null=True, blank=True,)
    filename = models.CharField(verbose_name="文件名", max_length=500, null=True, blank=True,)
    order = models.IntegerField(verbose_name="排序", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传人', null=True, blank=True, )
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='最后一次修改时间')

    class Meta:
        verbose_name = '资料管理'
        db_table = "ftp"
