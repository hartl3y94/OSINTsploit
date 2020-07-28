from django.db import models
from django.db.models import Model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    hibpkey = models.TextField(max_length=500, blank=True)

    hunterkey = models.TextField(max_length=500, blank=True)

    hlruname = models.TextField(max_length=500, blank=True)

    hlrpwd = models.TextField(max_length=500, blank=True)

    apilayerphone = models.TextField(max_length=500, blank=True)

    googlemapapikey = models.TextField(max_length=500, blank=True)

    macapikey = models.TextField(max_length=500, blank=True)

    ipstackkey = models.TextField(max_length=500, blank=True)

    virustotalkey = models.TextField(max_length=500, blank=True)
    
    shodankey = models.TextField(max_length=500, blank=True)
    
    emailrepkey = models.TextField(max_length=500, blank=True)

    victimips = models.TextField(max_length=100, blank=True)
    
    c_user = models.TextField(max_length=100, blank=True)

    xs = models.TextField(max_length=100, blank=True)        

    victimpublicip = models.TextField(max_length=500, blank=True)

    victimlocip = models.TextField(max_length=500, blank=True)

    victimlatitude = models.TextField(max_length=500, blank=True)

    victimlongitude = models.TextField(max_length=500, blank=True)

    victimuseragent = models.TextField(max_length=500, blank=True)

    clusterjson = models.FileField(default='cluster.json', upload_to='json/')

    metaimage = models.ImageField(default='default.jpg', upload_to='metadata/')

    def __str__(self):
        return f'{self.user.username}'
    
    def get_profile(self):
        return self.objects.all()

@receiver(post_save, sender=User)
def create_api_key(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_api_key(sender, instance, **kwargs):
    instance.profile.save()

    