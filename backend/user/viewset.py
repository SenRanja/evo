# encoding=utf-8
import json
from datetime import datetime
from django.http import JsonResponse as JR

from conf.errors import error_log_msg, success_msg
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters

from user.models import User
from user.serializer import UserSerializer, GroupSerializer

def format_date(date_string):
    # 将日期字符串解析为 datetime 对象
    date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    # 格式化日期为 YYYY-mm-dd 格式
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date

# DRF要求建立ViewSet

class UserViewSet(viewsets.ModelViewSet):
    # exclude 是过滤  stu_id != 'AnonymousUser'
    queryset = User.objects.exclude(stu_id='AnonymousUser').order_by('-create_time')
    serializer_class = UserSerializer

    # 【关键字搜索】
    # 参考链接: https://blog.csdn.net/weixin_42134789/article/details/111714018
    # 指定 搜索字段 的 模糊搜索、精确搜索
    # 如
    # http://127.0.0.1:8000/api/user/?search=%E7%94%B3
    # http://127.0.0.1:8000/api/user/?search=18536864913
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['id', 'stu_id', 'name', 'tel', 'id_card', 'email', 'role', ]

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)

        name = data["name"]
        pwd = data['password']
        stu_id = data['stu_id']
        tel = data['tel']
        id_card = data['id_card']
        email = data['email']
        role = data['role']

        # 注册超级管理员
        if role == "admin":
            user = User.objects.create_superuser(password=pwd, name=name, stu_id=stu_id, tel=tel, id_card=id_card,
                                                 email=email, role=role)
        else:
                user = User.objects.create_user(password=pwd, name=name, stu_id=stu_id, tel=tel, id_card=id_card,
                                                email=email, role=role)
        return JR(success_msg("created new user: {name}".format(name=name)))

    def list(self, request, *args, **kwargs):
        # 默认显示30个新用户
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for i in range(0, len(serializer.data)):
                # 遍历每一个 User
                serializer.data[i]["create_time"] = format_date(serializer.data[i]["create_time"])
                if serializer.data[i]["last_login"]!=None:
                    serializer.data[i]["last_login"] = format_date(serializer.data[i]["last_login"])
                else:
                    serializer.data[i]["last_login"] = "未登录"
                # 替换班级为 班级名
                class_list = []
                for single_class in serializer.data[i]["groups"]:
                    grp_obj = Group.objects.get(id=single_class)
                    class_list.append(grp_obj.name)
                serializer.data[i]["groups"] = class_list
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for i in range(0, len(serializer.data)):
            serializer.data[i]["create_time"] = format_date(serializer.data[i]["create_time"])
        return Response({'data': serializer.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 由于将 last_login 和 create_time 进行自定义处理了，此处DRF的PUT方法接受这两个参数，需要手动去除
        data = request.data
        data.pop('create_time')
        data.pop('last_login')
        serializer = self.get_serializer(instance, data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # 修改密码
        if 'pbkdf2_sha256$' not in data['password']:
            user = User.objects.get(id=data['id'])
            user.set_password(data['password'])
            user.save()
        return Response(serializer.data)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name',]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.role=="tea":
            queryset = user.groups.all()
        if user.role=="stu":
            queryset = user.groups.all()
        if user.role == "admin":
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        "返回该 group 的全部用户"
        ret_dict = dict()
        instance = self.get_object()
        ret_dict['group_name'] = instance.name
        ret_dict['users'] = []
        users_in_group = instance.user_set.all()
        for i in users_in_group:
            ret_dict['users'].append({
                "stu_id":i.stu_id,
                "name":i.name,
            })
        return JR(ret_dict)
