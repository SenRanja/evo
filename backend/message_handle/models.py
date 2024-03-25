from django.db import models


class Message(models.Model):
    '''消息管理'''
    # 发送人
    username = models.CharField(verbose_name="发送人（非User）", max_length=255, null=True, blank=True,)
    # 标题
    title = models.CharField(verbose_name="标题", max_length=500, null=True, blank=True, )
    # 正文
    text = models.TextField(verbose_name="正文", max_length=5000, null=True, blank=True,)
    # 创建时间
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', blank=True, null=True, )
    class Meta:
        verbose_name = "消息管理"
        db_table = "message"