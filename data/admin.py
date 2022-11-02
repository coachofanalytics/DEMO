from django.contrib import admin

from .models import FeaturedCategory,FeaturedSubCategory, ActivityLinks, FeaturedActivity, Interviews, Interview_Questions, JobRole #, DocUpload

'''
# Register your models here.

admin.site.register(DocUpload)
'''
admin.site.register(FeaturedCategory)
admin.site.register(FeaturedSubCategory)
admin.site.register(FeaturedActivity)
admin.site.register(ActivityLinks)
admin.site.register(Interviews)
admin.site.register(Interview_Questions)
admin.site.register(JobRole)
