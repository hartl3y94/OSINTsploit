# Generated by Django 3.0.5 on 2020-06-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0003_auto_20200521_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ratelimit',
            field=models.IntegerField(default=100, editable=False),
        ),
    ]
