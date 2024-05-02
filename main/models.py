from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.utils.text import slugify
from django.db.models.signals import pre_save
from .utils import unique_slug_generator,slug_pre_save_receiver
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# from tableauhyperapi import DatabaseName

User = get_user_model()
# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Service(models.Model):
    serial = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(default='training',max_length=254)
    slug = models.SlugField(default='slug',max_length=255)
    description = models.TextField(null=True, blank=True)
    sub_titles = models.TextField(null=True, blank=True)
    # executive_summary = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

# class ServiceCategory(models.Model):
#     pass
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, default=Service.objects.get_or_create(serial=1)[0].id)
#     name = models.CharField(max_length=254)
#     slug = models.SlugField(null=True, blank=True,unique=True)
#     description = models.TextField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_featured = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = "Service Categories"

#     def __str__(self):
#         return self.name

class Assets(TimeStampedModel):
    name = models.CharField(max_length=200)
    category = models.CharField(default='background',max_length=200,null=True, blank=True)
    image_string = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True,default='background')
    service_image =models.ImageField(null=True, blank=True, upload_to="images/",default='background')

    image_url = models.CharField(max_length=1000, null=True, blank=True,default='background')

    class Meta:
        verbose_name_plural = "Assets"

    @property
    def split_name(self):
        image_1=self.name.split("_")[0]
        image_2=self.name.split("_")[1]
        image_name=image_1,image_2

        return image_name

    def __str__(self):
        return self.name

# def servicecategory_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         if instance.name:
#             instance.slug = unique_slug_generator(instance)

# pre_save.connect(servicecategory_pre_save_receiver, sender=ServiceCategory)

