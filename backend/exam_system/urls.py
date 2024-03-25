# encoding=utf-8

from django.contrib import admin
from django.urls import path, include

# 前端
from exam_system.views import home
from django.views.generic import TemplateView

# DRF 路由
from rest_framework.routers import DefaultRouter
from user import viewset as user_viewset
from video import viewset as video_viewset
from ftp import viewset as ftp_viewset
from module import viewset as module_viewset
from question_manage import viewset as question_manage_viewset
from exam_manage import viewset as exam_manage_viewset
from exam_score import viewset as exam_score_viewset
from subject_manage import viewset as subject_manage_viewset
from notice import viewset as notice_viewset
from system_manage import viewset as system_manage_viewset
from message_handle import viewset as message_handle_viewset

# DRF 路由，全部模型汇聚至 DRF router
router = DefaultRouter()
router.register('user', user_viewset.UserViewSet)
router.register('group', user_viewset.GroupViewSet)
router.register('module', module_viewset.ModuleViewSet)
router.register('sub_module', module_viewset.SubModuleViewSet)
router.register('exam_question', question_manage_viewset.ExamQuestionViewSet)
router.register('exam_manage', exam_manage_viewset.ExamManageViewSet)
router.register('exam_manage_class', exam_manage_viewset.ExamManageClassViewSet)
router.register('exam_manage_question_database', exam_manage_viewset.ExamManage_QuestionDatabaseViewSet)
router.register('exam_score', exam_score_viewset.ExamScoreResultViewSet)
router.register('exam_score_subjective_result', exam_score_viewset.ExamSubjectiveResultViewSet)
router.register('subject', subject_manage_viewset.SubjectViewSet)
router.register('subject_group', subject_manage_viewset.SubjectClassViewSet)
# router.register('subject_staff_group', subject_manage_viewset.SubjectStaffGroupViewSet)
router.register('video', video_viewset.VideoViewSet)
router.register('ftp', ftp_viewset.FtpViewSet)
router.register('notice', notice_viewset.NoticeManageViewSet)
router.register('system_manage', system_manage_viewset.SystemManageViewSet)
router.register('message_handle', message_handle_viewset.MessageViewSet)


urlpatterns = [

    # 前端
    # path('', TemplateView.as_view(template_name='index.html')),
    # path('', home),

    # admin后台显示存在问题，暂未详细处理，不推荐使用
    # path('admin/', admin.site.urls),

    # DRF 路由 api
    path('api/', include(router.urls)),

    # 视频模块
    path('api/', include("video.urls")),

    # ftp模块
    path('api/', include("ftp.urls")),

    # 用户模块
    path('api/', include("user.urls")),

    # 公告模块
    path('api/', include("notice.urls")),

    # 试题管理模块
    # path('api/', include("question_manage.urls")),

    # 考试管理模块
    path('api/', include("exam_manage.urls")),

    # 试题模块
    path('api/', include("question_manage.urls")),

    # 成绩管理模块
    path('api/', include("exam_score.urls")),

    # 课程管理
    path('api/', include("subject_manage.urls")),

    # 系统监控模块
    path('api/', include("system_monitor.urls")),

    # license许可模块
    path('api/', include("license.urls")),

    # module 模块
    path('api/', include("module.urls")),

    # message_handle 模块
    path('api/', include("message_handle.urls")),
]
