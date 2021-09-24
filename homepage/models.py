from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=200)
    #image = models.ImageField(upload_to='images')
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    def __str__(self):
        return self.title