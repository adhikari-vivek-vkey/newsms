from django.db import models
from django.contrib.auth.models import User
import django
# Create your models here.


class LoanTypes(models.Model):
    amount = models.FloatField()
    disbursement_amount = models.FloatField()

    def __str__(self):
        return '{}'.format(self.disbursement_amount)


class Loans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(default=django.utils.timezone.now)
    repayment_status = models.IntegerField(default=0)
    loan_type = models.ForeignKey('LoanTypes', on_delete=models.CASCADE)


class Profile(models.Model):
    name = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(unique=True, null=True)
    preference = models.ForeignKey('Preferences', on_delete=models.CASCADE, null=True)
    preference_number = models.BigIntegerField(null=True)



class Preferences(models.Model):
    relation = models.TextField(unique=True)

    def __str__(self):
        return self.relation


class BankAccountDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.TextField(unique=True, null=True)