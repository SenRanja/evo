# encoding=utf-8

from rest_framework import serializers
from exam_manage.models import ExamManage, ExamManage_QuestionDatabase, ExamManageClass


# DRF要求建立序列化程序

class ExamManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamManage
        fields = '__all__'
        # fields = ['id', 'exam_name']

class ExamManageClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamManageClass
        fields = '__all__'

class ExamManage_QuestionDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamManage_QuestionDatabase
        fields = '__all__'
