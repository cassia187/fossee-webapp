from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Basic user registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Create your models here.
# Dataset Model used for storing dataset information and processing
class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"
    
class Equipment(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=255)
    flowrate = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name
    