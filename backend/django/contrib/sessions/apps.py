# encoding=utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SessionsConfig(AppConfig):
    name = 'django.contrib.sessions'
    verbose_name = _("Sessions")
