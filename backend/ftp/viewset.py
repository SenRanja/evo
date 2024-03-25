# encoding=utf-8
from conf.errors import success_msg
from django.http import JsonResponse as JR
from log.loguru_log import log_data
from ftp.models import Ftp
from rest_framework import viewsets, status
from ftp.serializer import FtpSerializer
from rest_framework.response import Response
from video.serializer import VideoSerializer

class FtpViewSet(viewsets.ModelViewSet):
    """Video视频API操作，支持 GET  POST  DELETE  PATCH或PUT 改动较大"""
    queryset = Ftp.objects.all().order_by('subject')
    serializer_class = FtpSerializer
    def create(self, request, *args, **kwargs):
        # 此处新增代码，默认将当前用户赋值给user字段
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        serializer.save(user=user)

        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return JR(success_msg("okok"))
