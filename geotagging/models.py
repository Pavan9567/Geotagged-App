from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GeotaggedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_data = models.TextField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}: {self.timestamp}"
    
class LoginUser(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
