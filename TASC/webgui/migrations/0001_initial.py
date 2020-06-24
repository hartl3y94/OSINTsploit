# Generated by Django 3.0.6 on 2020-05-19 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hibpkey', models.TextField(blank=True, max_length=500)),
                ('hunterkey', models.TextField(blank=True, max_length=500)),
                ('hlrlookupkey', models.TextField(blank=True, max_length=500)),
                ('googlemapapikey', models.TextField(blank=True, max_length=500)),
                ('macapikey', models.TextField(blank=True, max_length=500)),
                ('ipstackkey', models.TextField(blank=True, max_length=500)),
                ('virustotalkey', models.TextField(blank=True, max_length=500)),
                ('shodankey', models.TextField(blank=True, max_length=500)),
                ('emailrepkey', models.TextField(blank=True, max_length=500)),
                ('victimips', models.TextField(blank=True, max_length=100)),
                ('c_user', models.TextField(blank=True, max_length=100)),
                ('xs', models.TextField(blank=True, max_length=100)),
                ('victimpublicip', models.TextField(blank=True, max_length=500)),
                ('victimlocip', models.TextField(blank=True, max_length=500)),
                ('victimlatitude', models.TextField(blank=True, max_length=500)),
                ('victimlongitude', models.TextField(blank=True, max_length=500)),
                ('darkmode', models.BooleanField(default=False)),
                ('metaimage', models.ImageField(default='default.jpg', upload_to='metadata/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
