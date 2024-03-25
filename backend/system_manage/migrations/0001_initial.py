# Generated by Django 3.2.23 on 2024-03-12 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemManageSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_title', models.CharField(blank=True, max_length=600, null=True, verbose_name='主标题')),
                ('vice_title', models.CharField(blank=True, max_length=600, null=True, verbose_name='副标题')),
                ('login_title', models.CharField(blank=True, max_length=600, null=True, verbose_name='登录标题')),
            ],
            options={
                'verbose_name': '系统参数配置',
                'db_table': 'settings',
            },
        ),
    ]
