# Generated by Django 3.0.5 on 2020-06-16 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0033_auto_20200616_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ratelimit',
            field=models.IntegerField(default=100),
        ),
    ]
