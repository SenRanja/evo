# encoding=utf-8
from django.contrib.flatpages import views
from django.urls import path

urlpatterns = [
    path('<path:url>', views.flatpage, name='django.contrib.flatpages.views.flatpage'),
]
