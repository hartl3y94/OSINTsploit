# Generated by Django 3.0.5 on 2020-06-16 04:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0017_auto_20200616_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resetdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 4, 32, 37, 8205, tzinfo=utc)),
        ),
    ]
