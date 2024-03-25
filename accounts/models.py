from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import check_password as django_check_password

class Account(models.Model):
    class Gender(models.TextChoices):
        MALE = ('m', 'Male')
        FEMALE = ('f', 'Female')

    class AccountType(models.TextChoices):
        SAVING = ('s', 'Saving')
        CURRENT = ('c', 'Current')

    accountNo = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(111111111111), MaxValueValidator(999999999999)])
    name = models.CharField(max_length=200)
    fathers_name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=10)
    dob = models.DateField()
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    accountType = models.CharField(max_length=20, choices=AccountType.choices)
    profile_image = models.ImageField(upload_to='account_images/', blank=True, null=True)
    is_admin = models.BooleanField(default =False)
    password = models.CharField(max_length=50)
    accountOpened = models.DateTimeField(default=timezone.now)

    def check_password(self, raw_password):
        return raw_password == self.password

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    accountNo = models.ForeignKey(Account, on_delete=models.CASCADE)
    dateOfTransaction = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    debit = models.PositiveIntegerField(default=0)
    credit = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        last_transaction = Transaction.objects.filter(accountNo=self.accountNo).order_by('-dateOfTransaction').first()
        if last_transaction:
            self.balance = int(last_transaction.balance) + int(self.credit) - int(self.debit)
        else:
            self.balance = self.credit

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction for Account No. {self.accountNo}"
    
class Application(models.Model):
    APPLICATION_TYPE_CHOICES = [
        ('home_loan', 'Home Loan'),
        ('education_loan', 'Education Loan'),
    ]

    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    ]

    accountNo = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    fathers_name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    date_of_application = models.DateTimeField(default=timezone.now)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPE_CHOICES)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.accountNo}-{self.application_type}"