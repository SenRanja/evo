# encoding=utf-8
from django.urls import path
from license import views

urlpatterns = [
    # 获取许可时间
    path("get_license_time/", views.get_license_days_num),

    # 提交license
    path("submit_license/<str:license>/", views.submit_license),
]
