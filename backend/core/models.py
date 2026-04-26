from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.FloatField()
    category = models.CharField(max_length=100, blank=True, null=True)
    is_auto_categorized = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"


    

class Budget(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    monthly_limit = models.FloatField()
    current_spent = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} Budget"