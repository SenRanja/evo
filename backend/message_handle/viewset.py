# encoding=utf-8

from rest_framework import viewsets, filters
from message_handle.serializer import MessageSerializer
from message_handle.models import Message


# DRF要求建立ViewSet

class MessageViewSet(viewsets.ModelViewSet):
    """消息管理"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    filter_backends = [filters.SearchFilter, ]
    search_fields = ['username', 'title', 'text', 'creation_time', ]
