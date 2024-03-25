# encoding=utf-8

from rest_framework import serializers
from question_manage.models import ExamQuestion

# DRF要求建立序列化程序

class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = '__all__'
        # extra_kwargs = {
        #     'question_image_data': {'write_only': True}  # 标记该字段仅用于写入，不在序列化输出中显示
        # }
        def to_representation(self, instance):
            """默认不打印 question_image_data 字段，该字段仅在 create 和 update 有用"""
            representation = super().to_representation(instance)
            representation.pop('question_image_data', None)  # 从输出中移除 question_image_data
            return representation
