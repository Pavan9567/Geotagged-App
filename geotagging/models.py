from django.db import models

# Create your models here.
class GeotaggedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    extracted_data = models.TextField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}: {self.timestamp}"
