from django.db import models
from django.contrib.auth.models import User

class CropsHistory(models.Model):
    temp = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    ph_value = models.FloatField(null=True)
    moisture = models.FloatField(null=True)
    crop = models.CharField(max_length=256, null=True)
    user = models.ForeignKey(User,related_name="CropsHistory", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.crop
