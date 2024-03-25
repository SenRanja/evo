# encoding=utf-8
from django.urls import path
from ftp import views

urlpatterns = [
    # 流式HTTP播放视频文件
    # path("video/<str:video_path>/", views.serve_video),

    # 上传视频
    path("ftp_upload/", views.ftp_upload),

    # 根据 学科id 获取资料列表
    path("get_ftps_by_subject/<int:sid>/", views.get_ftps_by_subject),

    # 学生视角
    # 根据班级获取视频的可看学科
    # 【资料权限同视频】
    # path("get_video_subjects/"
]
