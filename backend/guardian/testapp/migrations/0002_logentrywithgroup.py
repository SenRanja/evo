# encoding=utf-8
# Generated by Django 1.9.9 on 2016-09-18 17:52
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('admin', '0001_initial'),
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntryWithGroup',
            fields=[
                ('logentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='admin.LogEntry')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            bases=('admin.logentry',),
        ),
    ]
