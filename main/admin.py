from django.contrib import admin
from .models import Investment
from .models import business

from .models import Assets,TeamMembers,Feedback,Description,Page,Team,Content,Service,SubService,News,Training,Pricing

# Register your models here.
admin.site.register(Assets)
admin.site.register(Feedback)
admin.site.register(Description)
admin.site.register(Page)
admin.site.register(Team)
admin.site.register(Content)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(News)
admin.site.register(Training)
admin.site.register(Pricing)
admin.site.register(TeamMembers)

admin.site.register(Investment)

admin.site.register(business)

