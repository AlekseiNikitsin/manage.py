from django.db import models

# Create your models here.
class Modellex2023(models.Model):
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    img = models.ImageField(upload_to='imgs')
class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')





