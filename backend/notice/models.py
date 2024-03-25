# encoding=utf-8
from django.contrib.auth.models import Group

from django.db import models

class NoticeManage(models.Model):
    '''公告管理'''
    # 标题
    title = models.CharField(verbose_name="标题", max_length=255, null=True, blank=True,)
    # 描述
    description = models.TextField(verbose_name="描述", max_length=2000, null=True, blank=True,)
    # 公告有效期
    valid_days = models.IntegerField(verbose_name='公告有效期', blank=True, null=True, )
    # auto_now_add=True 当对象第一次被创建时，字段的值被设置为当前日期和时间。该字段的值在对象创建后就不再更新。通常用于记录对象的创建时间。
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='公告创建时间')
    # auto_now=True 每次对象被保存时，字段的值都会被更新为当前日期和时间。即使对象未更改其他字段，也会更新该字段。通常用于记录对象的最后修改时间。
    last_modified_time = models.DateTimeField(auto_now=True, verbose_name='公告最新更新时间')
    # 是否归档
    is_archived = models.BooleanField(default=False, verbose_name='归档，不可见', blank=True, null=True, )

    class Meta:
        verbose_name = "公告管理"
        db_table = "notice"

class NoticeManageClass(models.Model):
    '''公告对应班级'''
    group_class = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='被公告的班级')
    notice_pk = models.ForeignKey(NoticeManage, on_delete=models.CASCADE, verbose_name='公告')

    class Meta:
        verbose_name = '公告对应班级'
        db_table = "notice_group_class"
