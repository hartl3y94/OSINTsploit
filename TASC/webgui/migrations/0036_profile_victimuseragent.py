# Generated by Django 3.0.5 on 2020-07-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0035_auto_20200624_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='victimuseragent',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
