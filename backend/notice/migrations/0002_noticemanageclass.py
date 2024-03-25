# encoding=utf-8
# Generated by Django 3.2.23 on 2024-02-22 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeManageClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_manage_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice.noticemanage', verbose_name='公告')),
                ('group_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='被公告的班级')),
            ],
            options={
                'verbose_name': '公告对应班级',
                'db_table': 'notice_group_class',
            },
        ),
    ]
