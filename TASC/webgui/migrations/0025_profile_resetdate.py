# Generated by Django 3.0.5 on 2020-06-16 04:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0024_remove_profile_resetdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resetdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 4, 36, 58, 504531, tzinfo=utc)),
        ),
    ]