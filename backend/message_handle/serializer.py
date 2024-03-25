# encoding=utf-8

from rest_framework import serializers
from message_handle.models import Message


# DRF要求建立序列化程序

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
