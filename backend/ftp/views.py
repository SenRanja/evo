# encoding=utf-8
import os
import time

from exam_system.settings import TEACHING_FTP_ROOT
from conf.errors import success_msg
from django.http import JsonResponse as JR
from ftp.models import Ftp
from subject_manage.models import Subject

def ftp_upload(request):
    user = request.user
    if user.role == 'tea' or user.role == 'admin':
        # 只有教师和admin用户才可以上传视频
        # title = request.POST.get('title')
        order: int = int(request.POST.get('order'))
        subject_id:int = int(request.POST.get('subject'))
        file = request.FILES['file']

        # 将文件保存到某位置
        ext = file.name.split('.')[-1]  # 获取文件后缀
        current_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        filename = "{current_time}-{title}-{subject_id}-{order}.{ext}".format(
            current_time=current_time,
            title=file.name,
            subject_id=str(subject_id),
            order=str(order),
            ext=ext,
        )
        file_path = os.path.join(TEACHING_FTP_ROOT, filename)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        new_video = Ftp.objects.create(
            subject=Subject.objects.get(id=subject_id),
            # subject=subject,
            title=file.name,
            filename=filename,
            order=order,
            user=user,
        )

        return JR(success_msg('okokk'))
    else:
        return JR({"msg":"当前用户非教职工权限"})


def get_ftps_by_subject(request, sid):
    user = request.user
    ret = []
    sub = Subject.objects.get(id=sid)
    ds = Ftp.objects.filter(subject=sub)
    for d in ds:
        ret.append({
            'id': d.id,
            'title': d.title,
            'filename': d.filename,
            'order': d.order,
            'user': d.user.name,
            'subject': sid,
        })
    ret_dict = success_msg("ok")
    ret_dict.update({'data': ret})
    return JR(ret_dict)