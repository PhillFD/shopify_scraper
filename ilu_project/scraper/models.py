from django.db import models

# Create your models here.
class Products(models.Model):
     title = models.CharField(max_length=64)

     def __str__(self):
          return f"{self.title}" 
