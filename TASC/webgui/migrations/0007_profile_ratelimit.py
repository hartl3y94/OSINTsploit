# Generated by Django 3.0.5 on 2020-06-15 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0006_remove_profile_ratelimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ratelimit',
            field=models.IntegerField(default=100, editable=False),
        ),
    ]