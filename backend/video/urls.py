# encoding=utf-8
from django.urls import path
from video import views

urlpatterns = [
    # 流式HTTP播放视频文件
    # path("video/<str:video_path>/", views.serve_video),

    # 上传视频
    path("video_upload/", views.video_upload),

    # 学生视角
    # 根据班级获取视频的可看学科
    path("get_video_subjects/", views.get_video_subjects),
    # 根据 学科id 获取视频列表
    path("get_video_by_subject/<int:sid>/", views.get_video_by_subject),

    # Nginx已做配置
    # http://shenyanjian.cn/static/media/
]
