from django.db import models

# Create your models here.
from django.utils import timezone

user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class APIkey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hibpkey = models.TextField(max_length=500, blank=True)
    googleapikey = models.TextField(max_length=500, blank=True)
    macapikey = models.TextField(max_length=500, blank=True)
    emailkey = models.TextField(max_length=500, blank=True)
    virustotalkey = models.TextField(max_length=500, blank=True)



@receiver(post_save, sender=User)
def create_api_key(sender, instance, created, **kwargs):
    if created:
        APIkey.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_api_key(sender, instance, **kwargs):
    instance.profile.save()
    