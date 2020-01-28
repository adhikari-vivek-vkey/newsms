from django.contrib import admin
from .models import Profile, BankAccountDetails, LoanTypes, Loans, Preferences
# Register your models here.

admin.site.register(Profile)
admin.site.register(BankAccountDetails)
admin.site.register(LoanTypes)
admin.site.register(Loans)
admin.site.register(Preferences)
