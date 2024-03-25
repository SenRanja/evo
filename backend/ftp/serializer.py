# encoding=utf-8

from ftp.models import Ftp
from rest_framework import serializers


# DRF要求建立序列化程序
class FtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ftp
        fields = '__all__'
