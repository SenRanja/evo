# encoding=utf-8
# Generated by Django 3.2.23 on 2024-01-27 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamManage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_name', models.CharField(default='未命名', max_length=150, verbose_name='考试命名')),
                ('exam_type', models.CharField(choices=[('考试', '考试'), ('模拟', '模拟')], max_length=10, verbose_name='考试类型')),
                ('start_time', models.DateTimeField(verbose_name='开始考试时间')),
                ('end_time', models.DateTimeField(verbose_name='结束考试时间')),
                ('duration', models.IntegerField(help_text='自动计算分钟', verbose_name='考试时长（分钟）')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='考试管理创建时间')),
                ('last_modified_time', models.DateTimeField(auto_now=True, verbose_name='考试管理最后一次修改时间')),
                ('max_score', models.IntegerField(verbose_name='满分值设置')),
                ('is_archived', models.BooleanField(default=False, verbose_name='考试管理封存（考试完了，永不可动）')),
            ],
            options={
                'verbose_name': '考试管理',
                'db_table': 'exam_manage',
            },
        ),
        migrations.CreateModel(
            name='ExamManageClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_manage_pk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam_manage.exammanage', verbose_name='考试管理的场次')),
                ('group_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='参加考试的班级')),
            ],
            options={
                'verbose_name': '考试场次对应班级',
                'db_table': 'exam_manage_group_class',
            },
        ),
        migrations.CreateModel(
            name='ExamManage_QuestionDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_database', models.CharField(blank=True, max_length=150, null=True, verbose_name='题库名称')),
                ('question_type', models.CharField(blank=True, choices=[('判断', '判断'), ('单选', '单选'), ('多选', '多选'), ('填空', '填空'), ('简答', '简答'), ('论述', '论述')], max_length=10, null=True, verbose_name='试题类型')),
                ('difficulty_level', models.CharField(blank=True, choices=[('easy', '简单'), ('middle', '中等'), ('hard', '困难')], max_length=15, null=True, verbose_name='难易程度')),
                ('question_num', models.IntegerField(blank=True, null=True, verbose_name='题目数量')),
                ('single_question_score', models.IntegerField(blank=True, null=True, verbose_name='单个题目分值设置')),
                ('exam_manage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam_manage.exammanage', verbose_name='考试管理的场次')),
            ],
            options={
                'verbose_name': '考试场次对应题库选择和配置',
                'db_table': 'exam_manage_question_database',
            },
        ),
    ]