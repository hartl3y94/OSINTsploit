# Generated by Django 3.0.3 on 2020-05-12 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0010_auto_20200512_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='censyssecret',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]