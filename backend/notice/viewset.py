# encoding=utf-8
from datetime import datetime

from rest_framework import viewsets

from notice.models import NoticeManage
from notice.serializer import NoticeManageSerializer

from lib.timeFormat import date_delta

# DRF要求建立ViewSet
from rest_framework.response import Response

def format_date(date_string):
    # 将日期字符串解析为 datetime 对象
    date_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    # 格式化日期为 YYYY-mm-dd 格式
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date


class NoticeManageViewSet(viewsets.ModelViewSet):
    """公告管理"""
    # 写为 order_by('creation_time') 是按照该字段从小到大排序，写作  order_by('-creation_time') 是从大到小排序
    # queryset = NoticeManage.objects.all().order_by('-creation_time')[:20]
    queryset = NoticeManage.objects.filter(is_archived=False).order_by('-creation_time')
    serializer_class = NoticeManageSerializer

    def list(self, request, *args, **kwargs):
        # 迎合VUE的需求，此处必须使用data字段封装 json list 格式的数据
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for i in range(0, len(serializer.data)):
                serializer.data[i]["creation_time"] = format_date(serializer.data[i]["creation_time"])
                serializer.data[i]["last_modified_time"] = format_date(serializer.data[i]["last_modified_time"])
                # 触发公告有效天数检测
                a = date_delta(serializer.data[i]["last_modified_time"])
                b = serializer.data[i]["valid_days"]
                if date_delta(serializer.data[i]["last_modified_time"]) > serializer.data[i]["valid_days"]:
                    nm = NoticeManage.objects.get(id=serializer.data[i]["id"])
                    nm.is_archived = True
                    nm.save()
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        for i in range(0, len(serializer.data)):
            serializer.data[i]["creation_time"] = format_date(serializer.data[i]["creation_time"])
            serializer.data[i]["last_modified_time"] = format_date(serializer.data[i]["last_modified_time"])
        return Response({'data': serializer.data})


