from django.contrib import admin

from .models import Balancesheet_categories,Balancesheet_category,Balancesheet_entry,BalanceSheet_Summary,exception_clients

# # Register your models here.
admin.site.register(Balancesheet_categories)
admin.site.register(Balancesheet_category)
admin.site.register(Balancesheet_entry)
admin.site.register(BalanceSheet_Summary)
admin.site.register(exception_clients)
# admin.site.register(Reporting)
