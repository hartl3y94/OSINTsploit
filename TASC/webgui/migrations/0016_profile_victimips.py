# Generated by Django 3.0.5 on 2020-05-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0015_profile_emailrepkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='victimips',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]
