from django.db import models

class Category(models.TextChoices):
    SPORT = "SPORT", 
    ENTERTAINMENT = "ENTERTAINMENT", 
    TRAVELING = "TRAVELING", 
    EATING_OUT = "EATING OUT",