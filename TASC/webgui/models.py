from django.db import models
from django.db.models import Model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hibpkey = models.TextField(max_length=500, blank=True)

    hunterkey = models.TextField(max_length=500, blank=True)

    hlrlookupkey = models.TextField(max_length=500, blank=True)

    googlemapapikey = models.TextField(max_length=500, blank=True)

    macapikey = models.TextField(max_length=500, blank=True)

    ipstackkey = models.TextField(max_length=500, blank=True)

    virustotalkey = models.TextField(max_length=500, blank=True)
    
    shodankey = models.TextField(max_length=500, blank=True)
    
    emailrepkey = models.TextField(max_length=500, blank=True)

    metaimage = models.ImageField(default='default.jpg', upload_to='metadata/')

    def __str__(self):
        return '{self.user.username}'

@receiver(post_save, sender=User)
def create_api_key(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_api_key(sender, instance, **kwargs):
    instance.profile.save()



    