# Generated by Django 2.2.1 on 2020-09-07 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_manage', '0004_studentassignmentanswers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='major',
        ),
        migrations.CreateModel(
            name='studentAssignmentMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_manage.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_manage.student')),
            ],
        ),
    ]
