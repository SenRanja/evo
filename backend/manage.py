# encoding=utf-8
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django import __version__
from lib.init import init

# 考试系统版本
__ES_VERSION__ = "0.0.1"

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    print("当前django运行版本: " + __version__)
    print("考试系统版本: " + __ES_VERSION__)

    # 初始化防破解程序
    print("初始化防破解程序 ... ")
    init()

    # django开始
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
