# encoding=utf-8

from rest_framework import serializers

from video.models import Video

# DRF要求建立序列化程序

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
