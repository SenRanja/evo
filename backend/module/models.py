# encoding=utf-8

from django.db import models

class Module(models.Model):
    '''菜单管理'''
    # menus 一级菜单
    menus = models.CharField(verbose_name="一级菜单", max_length=255, null=True, blank=True,)
    # 描述
    description = models.TextField(verbose_name="描述", max_length=1000, null=True, blank=True,)
    # 菜单图标
    icon = models.CharField(verbose_name="菜单图标", max_length=100, null=True, blank=True, )
    # 菜单排列次序
    order = models.IntegerField(verbose_name='菜单排列次序', null=True, blank=True, )
    class Meta:
        verbose_name = "功能板块"
        db_table = "modules"

class SubModule(models.Model):
    '''二级菜单管理'''
    # menus 一级菜单
    menus = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name='一级菜单', null=True, blank=True, )
    # menus 二级菜单
    child = models.CharField(verbose_name="二级菜单", max_length=255, null=True, blank=True,)
    # 描述
    description = models.TextField(verbose_name="描述", max_length=1000, null=True, blank=True,)
    # 前端路由
    frontpath = models.TextField(verbose_name="前端路由", max_length=1000, null=True, blank=True, )
    # 菜单图标
    icon = models.CharField(verbose_name="菜单图标", max_length=100, null=True, blank=True, )
    # 菜单排列次序
    order = models.IntegerField(verbose_name='菜单排列次序', null=True, blank=True, )
    # 角色可见，逗号分隔（没置入第三方表，外键关联，是为了可读性）
    role_can_get = models.TextField(verbose_name="角色可见", max_length=3000, null=True, blank=True, )
    class Meta:
        verbose_name = "二级菜单"
        db_table = "modules_sub"
        # 自定义权限
        permissions = [
            # (codename, description)
            ("custom_submodule_can_get", "用户或组可获取该菜单"),
        ]

class ModuleRole(models.Model):
    '''角色'''
    role = models.CharField(verbose_name="角色", max_length=255, null=True, blank=True,)
    class Meta:
        verbose_name = "角色"
        db_table = "modules_roles"