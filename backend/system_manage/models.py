# encoding=utf-8
from django.db import models

# Create your models here.
class SystemManageSetting(models.Model):
    '''系统参数配置'''
    main_title = models.CharField(verbose_name="主标题", max_length=600, null=True, blank=True, )
    vice_title = models.CharField(verbose_name="副标题", max_length=600, null=True, blank=True, )
    login_title = models.CharField(verbose_name="登录标题", max_length=600, null=True, blank=True, )

    cheat_mouse_out = models.IntegerField(verbose_name="鼠标移出屏幕次数", null=True, blank=True, )
    cheat_page_out = models.IntegerField(verbose_name="切屏次数", null=True, blank=True, )

    class Meta:
        verbose_name = '系统参数配置'
        db_table = "settings"