# Generated by Django 2.2.1 on 2020-11-01 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_manage', '0013_delete_studentassignmentanswers'),
    ]

    operations = [
        migrations.CreateModel(
            name='studentAssignmentAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.FileField(upload_to='assignmentsAnswers/')),
                ('mark', models.IntegerField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_manage.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_manage.student')),
            ],
        ),
    ]