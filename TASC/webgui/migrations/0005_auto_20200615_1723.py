# Generated by Django 3.0.5 on 2020-06-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0004_profile_ratelimit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ratelimit',
            field=models.IntegerField(default=1, editable=False),
        ),
    ]
