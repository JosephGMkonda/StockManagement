from django.db import models
from django.contrib.auth.models import User
from ProductManager.models import Products
from sellsmanagement.models import SellsProduct

class TrackProfits(models.Model):
    PERIOD_CHOICES = [
        ('month', 'Monthly'),
        ('week', 'Weekly'),
        ('day', 'Daily'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=5, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    profits = models.FloatField()

    def __str__(self):
        return f"{self.owner.username} - {self.period} - {self.start_date} to {self.end_date}"
