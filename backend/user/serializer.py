# encoding=utf-8

from rest_framework import serializers

from django.contrib.auth.models import Group
from user.models import User

# DRF要求建立序列化程序

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        '''由于使用DRF直接操作User，赋值密码时直接明文未哈希便存储在数据库中。
此处重改create，使其能以User.objects.create_user而非User.objects.create方法，从而调用set_passwd来哈希密码存储'''
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # 从validated_data中取出密码字段
        password = validated_data.pop('password', None)
        # 调用父类的update方法，将更新应用到用户实例
        instance = super().update(instance, validated_data)
        # 如果密码存在，则更新密码
        if password is not None:
            instance.set_password(password)  # 使用set_password方法哈希密码
            instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
