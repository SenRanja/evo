# encoding=utf-8
# Generated by Django 2.2.10 on 2020-02-05 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0003_auto_20190611_0440'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParentTestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChildTestModel',
            fields=[
                ('parent_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='testapp.ParentTestModel')),
                ('name', models.CharField(max_length=31)),
            ],
            bases=('testapp.parenttestmodel',),
        ),
    ]