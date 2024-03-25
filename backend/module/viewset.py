# encoding=utf-8
from module.serializer import ModuleSerializer, SubModuleSerializer
from rest_framework import viewsets
from module.models import Module, SubModule


# DRF要求建立ViewSet

class ModuleViewSet(viewsets.ModelViewSet):
    """功能板块"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class SubModuleViewSet(viewsets.ModelViewSet):
    """功能板块"""
    queryset = SubModule.objects.all()
    serializer_class = SubModuleSerializer