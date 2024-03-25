# encoding=utf-8
import json

from django.contrib.auth.models import Group

from django.http import JsonResponse as JR, request
from conf.errors import success_msg
from notice.models import NoticeManage, NoticeManageClass


def notice_list(request):
    ret = success_msg("ok")

    # ret_notice_list = []
    # notice_list = NoticeManage.objects.all().order_by('creation_time')
    # for notice in notice_list:
    #     ret_notice_list.append({
    #         ""
    #     })
    # ret = success_msg("ok")
    return JR(ret)

def notice_class_add(request):
    '''(公告, 班级) 对应关系增加'''
    data = json.loads(request.body)

    group_class_name = data["group_class"]
    group = Group.objects.get(name=group_class_name)
    notice = data['notice_pk']
    notice_obj = NoticeManage.objects.get(id=notice)

    NoticeManageClass.objects.create(group_class=group, notice_pk=notice_obj)
    return JR(success_msg("okok"))

def notice_class_del(request):
    '''(公告, 班级) 对应关系删除'''
    data = json.loads(request.body)

    group_class_name = data["group_class"]
    group = Group.objects.get(name=group_class_name)
    notice = data['notice_pk']
    notice_obj = NoticeManage.objects.get(id=notice)

    obj = NoticeManageClass.objects.get(group_class=group, notice_pk=notice_obj)
    obj.delete()
    return JR(success_msg("okok"))

