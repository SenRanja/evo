# encoding=utf-8

from rest_framework import serializers
from subject_manage.models import Subject, SubjectStaffGroup, SubjectClass


# DRF要求建立序列化程序

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectStaffGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectStaffGroup
        fields = '__all__'

class SubjectClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectClass
        fields = '__all__'
