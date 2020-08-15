from django.db import models
from django.contrib.auth.models  import User
from PIL import Image



# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(null=True, default='default.png', upload_to='profile_pics', blank=True )
    address = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
