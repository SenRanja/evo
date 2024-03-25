# encoding=utf-8
# 测试API
import mimetypes
import os
import time
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import FileResponse
from django.http import StreamingHttpResponse
from django.http import JsonResponse as JR

from conf.errors import success_msg, error_video_upload_is_not_staff_msg
from subject_manage.models import Subject, SubjectClass
from video.models import Video
from exam_system.settings import TEACHING_VIDEO_ROOT

# StreamingHttpResponse 通过流式传输的方式逐步将文件内容发送给客户端，而不是一次性将整个文件加载到内存中。这样可以避免在处理大文件时消耗大量内存。
# 当用户使用浏览器打开包含视频文件的页面时，浏览器会通过 HTTP 请求逐段地请求视频文件的内容。由于响应是逐段生成的，因此用户不会一次性将整个文件下载下来。相反，浏览器会逐段加载并播放视频。
# 这种方式对于大文件（如视频文件）是非常有效的，因为它减轻了服务器的负担，也降低了客户端对内存的需求。用户体验上，用户可以边加载边观看视频，而无需等待整个文件加载完成。

# 【暂时弃用】
def stream_video(request, video_path):
    # 此处不能使用with结构，with结构会在区域代码结束释放文件资源，不适合stream类型的分块传输
    # 构建视频文件的完整路径
    """目前由于前端控制条和此处后端无法完成 ”拖动进度“ 的问题，暂时搁置stream类型的分块传输方式"""
    video_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_path)
    content_type, encoding = mimetypes.guess_type(video_file_path)
    # 使用 with 语句确保文件在使用后被关闭
    video_file = open(video_file_path, 'rb')
    file_wrapper = FileWrapper(video_file)
    response = StreamingHttpResponse(file_wrapper, content_type=content_type)
    # 设置响应头，仅返回文件名，如 123.mp4
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(video_path)}'
    return response

# 【暂时弃用】
def serve_video(request, video_path):
    # 构建视频文件的完整路径
    video_file_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_path)
    # 使用 FileResponse 直接返回整个文件
    response = FileResponse(open(video_file_path, 'rb'), content_type='video/mp4')
    # 仅返回文件名，如 123.mp4
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(video_path)}'
    return response


def video_upload(request):
    user = request.user
    if user.role == 'tea' or user.role == 'admin':
        # 只有教师和admin用户才可以上传视频
        title = request.POST.get('title')
        order: int = int(request.POST.get('order'))
        subject_id:int = int(request.POST.get('subject'))
        file = request.FILES['file']

        # 将文件保存到某位置
        ext = file.name.split('.')[-1]  # 获取文件后缀
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        filename = "{current_time}-{id}-{name}-{title}-{subject_id}-{order}.{ext}".format(
            current_time=current_time,
            id=str(user.id),
            name=user.name,
            title=title,
            subject_id=str(subject_id),
            order=str(order),
            ext=ext,
        )
        file_path = os.path.join(TEACHING_VIDEO_ROOT, filename)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        new_video = Video.objects.create(
            subject=Subject.objects.get(id=subject_id),
            # subject=subject,
            title=title,
            filename=filename,
            order=order,
            user=user,
        )

        return JR(success_msg('okokk'))
    else:
        return JR(error_video_upload_is_not_staff_msg("当前用户非教职工权限"))

def get_video_subjects(request):
    user = request.user
    ret = []
    if user.role=='admin':
        scs = SubjectClass.objects.all()
        for sc in scs:
            ret.append({
                'subject_id': sc.subject.id,
                'subject': sc.subject.subject,
                'description': sc.subject.description,
            })
    else:
        groups = user.groups.all()
        for single_group in groups:
            scs = SubjectClass.objects.filter(group=single_group)
            for sc in scs:
                ret.append({
                    'subject_id': sc.subject.id,
                    'subject': sc.subject.subject,
                    'description': sc.subject.description,
                })
    ret_dict = success_msg("ok")
    ret_dict.update({'data': ret})
    return JR(ret_dict)

def get_video_by_subject(request, sid):
    user = request.user
    ret = []
    sub = Subject.objects.get(id=sid)
    vs = Video.objects.filter(subject=sub).order_by('order')
    for v in vs:
        ret.append({
            'id': v.id,
            'filename': v.filename,
            'order': v.order,
            'user': v.user.name,
            'title': v.title,
        })
    ret_dict = success_msg("ok")
    ret_dict.update({'data': ret})
    return JR(ret_dict)