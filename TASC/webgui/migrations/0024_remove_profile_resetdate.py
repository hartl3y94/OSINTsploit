# Generated by Django 3.0.5 on 2020-06-16 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0023_auto_20200616_0436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='resetdate',
        ),
    ]