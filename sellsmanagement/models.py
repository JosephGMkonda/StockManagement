from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.




class SellsProduct(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    qauntity = models.IntegerField()
    date = models.DateField(default=now)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=225)
    

    def __str__(self):
        return self.name

    class Meta:
        ordering:['-date']

class SellsProductCategory(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name

    class Meta:
        ordering:['alphabet']





