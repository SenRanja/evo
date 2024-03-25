# encoding=utf-8
from django.urls import path
from system_monitor import views

urlpatterns = [
    path("get_system_info/", views.system_display),
    path("index_statistics/", views.index_statistics),
]
