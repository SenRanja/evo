# encoding=utf-8

import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from django.http import JsonResponse as JR
from system_manage.models import SystemManageSetting
from system_manage.serializer import SystemManageSerializer
from rest_framework.permissions import AllowAny

# DRF要求建立ViewSet

class SystemManageViewSet(viewsets.ModelViewSet):
    """学科管理"""
    queryset = SystemManageSetting.objects.all()
    serializer_class = SystemManageSerializer
    permission_classes = [AllowAny]  # 允许无鉴权访问
