from django.db import models
from django.contrib.auth.models  import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_image = models.ImageField(null=True, default='default.png', upload_to='profile_pics', blank=True )
    address = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
