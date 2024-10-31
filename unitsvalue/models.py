# unitsvalue/models.py

from django.db import models
from django.utils import timezone

class Fund(models.Model):
    url = models.URLField(unique=True) 
    name = models.CharField(max_length=100, null=True) 
    created_at = models.DateTimeField(default=timezone.now, null=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True, null=True)       # Automatically set on update

    def __str__(self):
        return self.url

class LivePercentUnit(models.Model):
    funds = models.ForeignKey(Fund, on_delete=models.CASCADE, related_name='LivePercentUnit')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, null=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True, null=True)       # Automatically set on update

    def __str__(self):
        return self.text

class PercentUnit(models.Model):
    funds = models.ForeignKey(Fund, null=True, on_delete=models.CASCADE)
    percent_unit = models.FloatField()
    datetime = models.CharField(max_length=10)  # Adjust length based on your format
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True, null=True)       # Automatically set on update
    deleted_at = models.DateTimeField(null=True, blank=True)  # For soft deletion

    def __str__(self):
        return f"{self.funds.name} - {self.percent_unit} on {self.datetime}"