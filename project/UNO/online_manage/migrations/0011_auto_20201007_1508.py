# Generated by Django 2.2.1 on 2020-10-07 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_manage', '0010_auto_20200924_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lectures',
            name='uploadTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
