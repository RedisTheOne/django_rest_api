# Generated by Django 3.1.7 on 2021-03-30 08:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 30, 8, 11, 55, 239752, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='comment',
            name='username',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
