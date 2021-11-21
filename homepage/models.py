from django.db import models
import os

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='images')
    # image = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)
    image = models.ImageField(upload_to="users/", blank=True)
    print("what the hell", image)

    def __str__(self):
        return self.title
