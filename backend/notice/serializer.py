# encoding=utf-8

from rest_framework import serializers

from notice.models import NoticeManage

# DRF要求建立序列化程序

class NoticeManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeManage
        fields = '__all__'
