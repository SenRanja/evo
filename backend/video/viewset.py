# encoding=utf-8
from conf.errors import success_msg
from django.http import JsonResponse as JR
from log.loguru_log import log_data
from rest_framework import viewsets, status
from rest_framework.response import Response
from video.models import Video
from video.serializer import VideoSerializer


# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# DRF要求建立ViewSet
# @csrf_exempt  基于普通view使用此装饰器
# @method_decorator(csrf_exempt, name='dispatch')  基于viewset使用此装饰器
# @method_decorator(csrf_exempt, name='dispatch')
class VideoViewSet(viewsets.ModelViewSet):
    """Video视频API操作，支持 GET  POST  DELETE  PATCH或PUT 改动较大"""
    queryset = Video.objects.all().order_by('subject').order_by('order')
    serializer_class = VideoSerializer

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

    # def update(self, request, *args, **kwargs):
        '''根据DRF的代码，PUT和PATCH是 change 权限支持的两个HTTP方法。报文如下即可。

        PUT /api/video/32/ HTTP/1.1
Cookie: session_id=tkng3l34l8aiv4twbhu4gur9uvk9askb; session_id=tkng3l34l8aiv4twbhu4gur9uvk9askb
Content-Type: application/json
User-Agent: PostmanRuntime/7.36.1
Accept: */*
Cache-Control: no-cache
Postman-Token: fc9047bf-a518-4d65-ae61-937cf93cfa64
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: close
Content-Length: 47

{
    "id": 32,
    "name": "5654gogo2222"
}
        '''
        # partial = kwargs.pop('partial', False)
        # instance = self.get_object()
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}
        #
        # return JR(success_msg("change okok"))

    def destroy(self, request, *args, **kwargs):
        '''仅支持返回HttpResponse或Response（这是drf默认渲染页面），不支持自定义返回方法（如json）'''
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return JR(success_msg("delete ok"))
        except Exception as err:
            user_id = str(request.user.id)
            username = request.user.name
            err_msg = user_id + username + "delete failed, plz certify the obj exists. {ERR}".format(ERR=str(err))
            log_data.error(err_msg)
            return JR(success_msg(err_msg))
