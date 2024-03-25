# encoding=utf-8
from exam_score.models import ExamScoreResult, ExamSubjectiveResult
from rest_framework import serializers

# DRF要求建立序列化程序

class ExamScoreResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamScoreResult
        fields = '__all__'

class ExamSubjectiveResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubjectiveResult
        fields = '__all__'
