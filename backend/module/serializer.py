# encoding=utf-8

from rest_framework import serializers
from module.models import Module, SubModule


# DRF要求建立序列化程序

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class SubModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubModule
        fields = '__all__'