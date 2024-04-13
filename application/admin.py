from django.contrib import admin

from .models import XInvestmentContent,XInvestmentStrategy,Balancesheet_categories,Balancesheet_category,Balancesheet_entry,BalanceSheet_Summary

# # Register your models here.
admin.site.register(Balancesheet_categories)
admin.site.register(Balancesheet_category)
admin.site.register(Balancesheet_entry)
admin.site.register(BalanceSheet_Summary)

admin.site.register(XInvestmentStrategy)
admin.site.register(XInvestmentContent)
# admin.site.register(Reporting)
