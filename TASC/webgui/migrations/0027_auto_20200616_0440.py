# Generated by Django 3.0.5 on 2020-06-16 04:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0026_auto_20200616_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resetdate',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 16, 4, 40, 51, 582240)),
        ),
    ]
