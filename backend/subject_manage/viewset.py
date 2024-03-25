# encoding=utf-8

import json

from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.response import Response

from django.http import JsonResponse as JR
from subject_manage.models import Subject, SubjectStaffGroup, SubjectClass
from subject_manage.serializer import SubjectSerializer, SubjectStaffGroupSerializer, SubjectClassSerializer


# DRF要求建立ViewSet

class SubjectViewSet(viewsets.ModelViewSet):
    """学科管理"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def update(self, request, *args, **kwargs):
        # 针对 groups 字段，对viewset的 更新动作 进行变动
        data = request.data

        # 学科 -- 班级
        class_groups = data['groups']
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        SubjectClass.objects.filter(subject=instance).delete()
        if type(class_groups) != list:
            # 考虑 class_groups 是字符串类型，如 "企信,天津职业技术师范大学,17070144"
            if ',' not in class_groups or '，' not in class_groups:
                class_groups = class_groups+","
            if ',' in class_groups:
                class_groups = class_groups.split(',')
            if '，' in class_groups:
                class_groups = class_groups.split('，')
        for input_class in class_groups:
            if Group.objects.filter(name=input_class).exists():
                grp = Group.objects.get(name=input_class)
                sc_obj = SubjectClass.objects.create(group=grp, subject=instance)
                sc_obj.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role == "admin":
            # admin获取subject不走本viewset路由
            queryset = Subject.objects.all()
        elif user.role == "tea":
            queryset = []
            # 对学生用户，只返回班级有权限的课程
            groups = user.groups.all()
            for g in groups:
                g_s = SubjectClass.objects.filter(group=g)
                for s in g_s:
                    queryset.append(s.subject)
        elif user.role == "stu":
            queryset = []
            # 对学生用户，只返回班级有权限的课程
            groups = user.groups.all()
            for g in groups:
                g_s = SubjectClass.objects.filter(group=g)
                for s in g_s:
                    queryset.append(s.subject)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # 提取学科信息
        # subject_data = request.data.copy()

        # 创建学科对象序列化
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 若使用自定义方法保存，如 serializer.save ，则注销本行代码
        self.perform_create(serializer)

        # 学科 -- django默认Group 方式已弃用
        # # 提取学科名字
        # subject_name = subject_data.get('subject')
        # # 创建学科组，组名同学科名
        # group_name = subject_name
        # group = Group.objects.create(name=group_name)
        # # 将新创建的组设置为学科的 staff_group 外键
        # subject = serializer.save(staff_group=group)

        # 返回成功响应
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 废弃
class SubjectStaffGroupViewSet(viewsets.ModelViewSet):
    """学科管理"""
    queryset = SubjectStaffGroup.objects.all()
    serializer_class = SubjectStaffGroupSerializer


class SubjectClassViewSet(viewsets.ModelViewSet):
    """视频的 班级-学科 对应关系"""
    queryset = SubjectClass.objects.all()
    serializer_class = SubjectClassSerializer
