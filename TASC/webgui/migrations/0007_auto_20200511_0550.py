# Generated by Django 3.0.3 on 2020-05-11 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0006_profile_builtwithkey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='builtwithkey',
            new_name='wappalyzerkey',
        ),
    ]
