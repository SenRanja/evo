# encoding=utf-8

# from exam_manage.apps import ExamManageConfig
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
import json
from datetime import datetime

from django.contrib.auth.models import Group
from exam_manage.serializer import ExamManageSerializer, ExamManageClassSerializer, ExamManage_QuestionDatabaseSerializer
from guardian.shortcuts import get_objects_for_user
from rest_framework import viewsets, status, filters
from exam_manage.models import ExamManage, ExamManageClass, ExamManage_QuestionDatabase
from django.http import JsonResponse as JR

# DRF要求建立ViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.settings import api_settings
from lib.timeFormat import format_date, UTC_2_CN_TIME


class ExamManageViewSet(viewsets.ModelViewSet):
    """考试管理
    Django默认所有用户有view权限，大家的权限表初始默认是没有明写view权限，但是实际上可以看其他app的数据。
    此处对list方法进行权限校验，仅允许明确赋予view权限的用户查看"""

    queryset = ExamManage.objects.all().order_by('-start_time')
    serializer_class = ExamManageSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = ['exam_name', 'exam_type', 'max_score', 'is_archived', 'start_time', 'end_time', 'creation_time', 'last_modified_time', ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        start_time = format_date(serializer.data["start_time"]).replace(" ",'T')
        end_time = format_date(serializer.data["end_time"]).replace(" ",'T')
        exam_type = serializer.data["exam_type"]
        exam_name = serializer.data["exam_name"]
        multiple_half = serializer.data["multiple_half"]
        return JR(
            {
                "exam_type": exam_type,
                "exam_name": exam_name,
                "start_time": start_time,
                "end_time": end_time,
                "multiple_half": multiple_half,
            })
        # return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for i in range(0, len(serializer.data)):
                # 增加考试指定班级 class_groups
                class_groups = [ i.group_class.name for i in ExamManageClass.objects.filter(exam_manage_pk=serializer.data[i]["id"])]
                serializer.data[i]["class_groups"] = class_groups
                # 格式化时间
                serializer.data[i]["start_time"] = format_date(serializer.data[i]["start_time"])
                serializer.data[i]["end_time"] = format_date(serializer.data[i]["end_time"])
                serializer.data[i]["creation_time"] = format_date(serializer.data[i]["creation_time"])
                serializer.data[i]["last_modified_time"] = format_date(serializer.data[i]["last_modified_time"])
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # 针对 class_groups 字段，对viewset的 更新动作 进行变动
        data = request.data

        # 时间格式化
        # UTC_2_CN_TIME
        if 'T' in data['start_time'] and 'Z' in data['start_time']:
            data['start_time'] = UTC_2_CN_TIME(data['start_time'])
        if 'T' in data['end_time'] and 'Z' in data['end_time']:
            data['end_time'] = UTC_2_CN_TIME(data['end_time'])

        # 考试 -- 班级
        class_groups = data['class_groups']
        partial = kwargs.pop('partial', False)
        # instance 是 ExamManage 对象
        instance = self.get_object()
        # emc 获取对应考试的全部 ExamManageClass 对象
        ExamManageClass.objects.filter(exam_manage_pk=instance).delete()
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
                emc_obj = ExamManageClass.objects.create(group_class=grp, exam_manage_pk=instance)
                emc_obj.save()

        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        # update方法 的附属方法
        serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        # 时间格式化
        # UTC_2_CN_TIME
        if 'T' in data['start_time'] and 'Z' in data['start_time']:
            data['start_time'] = UTC_2_CN_TIME(data['start_time'])
        if 'T' in data['end_time'] and 'Z' in data['end_time']:
            data['end_time'] = UTC_2_CN_TIME(data['end_time'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    # 取消查看权限的方法
    # def check_permissions(self, request):
    #     # if self.action == 'retrieve':
    #         # 如果是查看单个对象的请求，抛出权限异常
    #     if self.action == 'list':
    #         raise PermissionDenied()
    #     return super().check_permissions(request)
    # 如果需要其他操作，可以重写其他方法，比如 list、create、update、destroy 等
    # def get_queryset(self):
    #     user = self.request.user

        # 对象级权限 失败，暂不细究
        # 使用 django-guardian 的 get_objects_for_user 函数
        # queryset = self.queryset
        # queryset_with_permissions = [
        #     obj for obj in queryset if user.has_perm('view_exammanage', obj)
        # ]
        # return queryset_with_permissions

        # 模型级权限
        # queryset = get_objects_for_user(user, 'exam_manage.view_exammanage', klass=ExamManage)
        # return queryset

    # def list(self, request, *args, **kwargs):
        # 想不硬编码 找到应用的权限，但是太繁琐了，还是适合直接硬编码找权限
        # codename = "view_exammanage"
        # app_label = ExamManageConfig.name
        # content_type = ContentType.objects.get(app_label=app_label)
        # permission = Permission.objects.get(content_type=content_type, codename=codename)

        # 对象级权限，参考self.get_queryset()
        # queryset = self.get_queryset()
        # serializer = self.get_serializer(queryset, many=True)

        # 返回全部
        # serializer = self.get_serializer(self.queryset, many=True)
        # return Response(serializer.data)

        # 如下代码已弃用，仅是应用级权限，非对象级权限
        # if user.has_perm('exam_manage.view_exammanage'):
        #     queryset = self.filter_queryset(self.get_queryset())
        #     page = self.paginate_queryset(queryset)
        #     if page is not None:
        #         serializer = self.get_serializer(page, many=True)
        #         return self.get_paginated_response(serializer.data)
        #
        #     # 如果指定 list 方法过滤数据
        #     # six_months_ago = timezone.now() - timedelta(days=180)
        #     # queryset = ExamManage.objects.filter(created_at__gte=six_months_ago, created_by=user)
        #     serializer = self.get_serializer(queryset, many=True)
        #     return Response(serializer.data)
        # else:
        #     raise PermissionDenied()

class ExamManageClassViewSet(viewsets.ModelViewSet):
    """考试管理
    Django默认所有用户有view权限，大家的权限表初始默认是没有明写view权限，但是实际上可以看其他app的数据。
    此处对list方法进行权限校验，仅允许明确赋予view权限的用户查看"""

    queryset = ExamManageClass.objects.all()
    serializer_class = ExamManageClassSerializer

class ExamManage_QuestionDatabaseViewSet(viewsets.ModelViewSet):
    """考试管理
    Django默认所有用户有view权限，大家的权限表初始默认是没有明写view权限，但是实际上可以看其他app的数据。
    此处对list方法进行权限校验，仅允许明确赋予view权限的用户查看

    每次变动 某次 考试--题库 对应关系，触发自动修改考试 ExamManage 的 max_score 满分字段"""
    # 此处为了直观，未在源代码中修改，故将不同HTTP协议处理方法复制此处修改

    queryset = ExamManage_QuestionDatabase.objects.all().order_by('question_type')
    serializer_class = ExamManage_QuestionDatabaseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # 查询考试对应试题设置分值列表不需要使用分页系统
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        exam_id = request.query_params.get('exam_id')
        em_obj = ExamManage.objects.get(id=exam_id)
        emqd = ExamManage_QuestionDatabase.objects.filter(exam_manage=em_obj)
        ret = []
        for i in emqd:
            ret.append(
                {
                    'exam_manage': i.exam_manage.id,
                    'question_database': i.question_database,
                    'question_type': i.question_type,
                    'difficulty_level': i.difficulty_level,
                    'question_num': i.question_num,
                    'single_question_score': i.single_question_score,
                 }
            )
        # serializer = self.get_serializer(queryset, many=True)
        return Response({'data': ret})
        # return Response({'data': serializer.data})

    def update_exam_manage_max_score(self, data):
        # 每次变动 某次 考试--题库 对应关系，触发自动修改考试 ExamManage 的 max_score 满分字段
        exam_manage_id = data["exam_manage"]
        # 根据考场id过滤出 考场--题目设置
        EMQD_obj_list = ExamManage_QuestionDatabase.objects.filter(exam_manage_id=exam_manage_id)
        # 计算满分
        max_score = 0
        for single_obj in EMQD_obj_list:
            max_score = max_score + single_obj.question_num * single_obj.single_question_score
        # 更新考试满分
        exam_obj = ExamManage.objects.get(id=exam_manage_id)
        exam_obj.max_score = max_score
        exam_obj.save()


    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 更新考试满分
        self.update_exam_manage_max_score(data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # 更新考试满分
        self.update_exam_manage_max_score(data)

        return Response(serializer.data)