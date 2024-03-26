#!/bin/bash

/usr/local/bin/python /app/manage.py makemigrations user video notice question_manage exam_manage exam_score license subject_manage module system_manage system_monitor ftp message_handle && /usr/local/bin/python /app/manage.py migrate
/usr/local/bin/python /app/init_default_admin.py
uwsgi --ini /app/uwsgi.ini
