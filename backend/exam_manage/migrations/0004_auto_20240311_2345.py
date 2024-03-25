# Generated by Django 3.2.23 on 2024-03-11 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_manage', '0003_auto_20240304_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exammanage',
            name='max_score',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='满分值设置'),
        ),
        migrations.AlterField(
            model_name='exammanage_questiondatabase',
            name='single_question_score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='单个题目分值设置'),
        ),
    ]
