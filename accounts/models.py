from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Account(models.Model):
    class Gender(models.TextChoices):
        MALE = ('m','male')
        FEMALE = ('f','female')
    class Account(models.TextChoices):
        MALE = ('s','saving')
        FEMALE = ('c','current')
    accountNo = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(111111111111),MaxValueValidator(999999999999)])
    name = models.CharField(max_length=200)
    dob = models.DateField()
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    accountType = models.CharField(max_length=20, choices=Account.choices)
