# encoding=utf-8

from rest_framework import serializers
from system_manage.models import SystemManageSetting


# DRF要求建立序列化程序

class SystemManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemManageSetting
        fields = '__all__'
