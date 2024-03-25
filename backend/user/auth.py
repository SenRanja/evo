# encoding=utf-8
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import User

# 自定义auth认证方式
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 允许根据传入的username（这里实际是手机号或学号）来查询用户。
        try:
            # user = User.objects.get(Q(stu_id=username) | Q(tel=username) | Q(email=username) | Q(id_card=username))
            user = User.objects.get(Q(stu_id=username) | Q(tel=username))
        except User.DoesNotExist:
            return None

        # 使用 AbstractUser 提供的 check_password 方法验证密码
        if user.check_password(password):
            return user
        return None
