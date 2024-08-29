from django.contrib import admin
from .models import Asset, Feedback, Description, Page, Team, Content, Service, SubService, News

# Register your models here.
admin.site.register(Asset)
admin.site.register(Feedback)
admin.site.register(Description)
admin.site.register(Page)
admin.site.register(Team)
admin.site.register(Content)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(News)
