from django.db import models
from datetime import datetime, date
from decimal import *
from enum import unique
from django.shortcuts import redirect, render
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.contrib.auth import get_user_model

#------------create models here----------------
class Balancesheet_categories(models.Model):
    CATEGORY_TYPES = [
        ("assets", 'Asset'),
        ("liability", 'Liability'),
        ("equity", 'Equity'),
    ]

    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255, choices=CATEGORY_TYPES, default='assets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('name', 'category_type')
        verbose_name_plural = 'Balance Sheet Categories'

    def __str__(self):
        return f"{self.name} ({self.category_type})"

class Balancesheet_category(models.Model):
    CATEGORY_TYPES = [
        ("assets", 'Asset'),
        ("liability", 'Liability'),
        ("equity", 'Equity'),
    ]

    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=255, choices=CATEGORY_TYPES, default='assets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('name', 'category_type')
        verbose_name_plural = 'Balance Sheet Categories'

    def __str__(self):
        return f"{self.name} ({self.category_type})"  

class BalanceSheet_Summary(models.Model):
    date = models.DateField(default=timezone.now)             

    @property
    def total_assets(self):
        return self.entries.filter(category__category_type='Asset').aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def total_liabilities(self):
        return self.entries.filter(category__category_type='Liability').aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def total_equity(self):
        return self.entries.filter(category__category_type='Equity').aggregate(models.Sum('amount'))['amount__sum'] or 0
        
    class Meta:
        verbose_name_plural = 'Balance Sheets'
        ordering = ["-date"]  # Corrected to lowercase

    def __str__(self):
        return f"Balance Sheet as of {self.date}"

class Balancesheet_entry(models.Model):
    balance_sheet = models.ForeignKey('BalanceSheet_Summary',on_delete=models.CASCADE,related_name='entries') 
    category = models.ForeignKey('Balancesheet_category',on_delete=models.CASCADE) 
    amount= models.DecimalField(max_digits=20,decimal_places=2)
    class Meta:
        verbose_name_plural='Balance Sheet Entries'

    def __str__(self):
        return f"{self.category.name}:{self.amount}"   
  

class items_entry(models.Model):
    items_id = models.AutoField(primary_key=True)
    items_name = models.CharField(max_length=255)
    items_category = models.CharField(max_length=255)
    items_purchase_date = models.DateField()
    items_Quantity = models.IntegerField()
    items_price = models.IntegerField()
    items_itemName = models.CharField(max_length=255)
    items_flag = models.BooleanField(max_length=255)


    def __str__(self) -> str:
        return f'items_ID: (self.items_id)'

class exception_user(models.Model):
    exception_id = models.AutoField(primary_key=True)
    exception_date = models.DateTimeField()
    exception_week = models.IntegerField()
    comments = models.CharField(max_length=255)
    exception_type_id = models.IntegerField()
    project_user_id = models.IntegerField()
    project_user_rts_id = models.IntegerField()
    exception_flag = models.BooleanField(default=False)
    pitch_flag = models.BooleanField(default=False)
    late_night = models.IntegerField()
    vacations = models.IntegerField()

    def __str__(self) :
        return f"exception_id: {self.exception_id}"
    






