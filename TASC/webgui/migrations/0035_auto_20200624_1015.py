# Generated by Django 3.0.5 on 2020-06-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webgui', '0034_auto_20200616_0449'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='hlrlookupkey',
            new_name='apilayerphone',
        ),
        migrations.AddField(
            model_name='profile',
            name='hlrpwd',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='hlruname',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
