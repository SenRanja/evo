# encoding=utf-8
# Generated by Django 3.2.23 on 2024-01-31 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0005_auto_20240131_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submodule',
            options={'permissions': [('custom_submodule_can_get', '用户或组可获取该菜单')], 'verbose_name': '二级菜单'},
        ),
    ]