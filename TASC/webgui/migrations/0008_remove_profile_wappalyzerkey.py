# Generated by Django 3.0.3 on 2020-05-11 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0007_auto_20200511_0550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='wappalyzerkey',
        ),
    ]
