from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class account(models.Model):
    GENDER_CHOICE=(
        ('m','male'),
        ('f','female')
    )
    ACCOUNT_TYPE=(
        ('s','saving'),
        ('c','current')
    )
    accountNo = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(1),MaxValueValidator(12)])
    name = models.CharField(max_lenght=200)
    dob = models.DateField()
    email = models.EmailField(max_length=200)
    gender = models.CharField(choises=GENDER_CHOICE)
    accountType = models.CharField(choises=ACCOUNT_TYPE)
