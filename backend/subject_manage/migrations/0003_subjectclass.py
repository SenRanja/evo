# Generated by Django 3.2.23 on 2024-03-10 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('subject_manage', '0002_subjectstaffgroup_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='班级')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='subject_manage.subject', verbose_name='学科')),
            ],
            options={
                'verbose_name': '学科--班级 对应关系',
                'db_table': 'subject_group',
            },
        ),
    ]
