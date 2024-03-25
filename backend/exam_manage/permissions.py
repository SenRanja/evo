# encoding=utf-8
from django.contrib.auth.backends import BaseBackend

# 目前没用，取消settings的该配置，暂未细究
class ExamManageCustomPermissionBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        # 取消用户对特定 app 的 view 权限
        if perm == 'view' and obj and obj._meta.app_label == 'exam_manage':
            return False
        res_perm = super().has_perm(user_obj, perm, obj)
        return res_perm
