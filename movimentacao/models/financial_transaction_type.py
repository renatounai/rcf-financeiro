from django.db import models


class FinancialTransactionType(models.TextChoices):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"
