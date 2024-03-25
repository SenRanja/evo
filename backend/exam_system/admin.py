# encoding=utf-8
from django.contrib import admin
from django.contrib.auth.models import Group

from user.models import User


class UserAdmin(admin.ModelAdmin):
    # 有 list_display 会直接显示数据
    list_display = ('name', 'username', 'tel',)
    # 搜索栏
    search_fields = ('name', 'username', 'tel',)
    # 显示字段
    # fields  = ('name', 'email')
    fieldsets = (
        ['Main', {
            'fields': ('name', 'username', 'tel',),
        }],
        # 添加时折叠
        ['Advance', {
            'classes': ('collapse',),  # CSS
            'fields': ('id_card',),
        }]
    )


# admin.site.register(User, UserAdmin)
admin.site.register([Group, User])
