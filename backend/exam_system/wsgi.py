# encoding=utf-8
"""
WSGI config for exam_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/

uwsgi只能在linux上运行，windows上无法运行uwsgi（pip安装报错）
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')

application = get_wsgi_application()
