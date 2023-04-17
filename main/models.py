from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

# from tableauhyperapi import DatabaseName

User = get_user_model()
# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Service(models.Model):
    serial = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(default='training',max_length=254)
    slug = models.SlugField(default='slug',max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)


class CourseCategory(models.Model):
    name = models.CharField(max_length=254)

    class Meta:
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    serial = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    subcategory = models.CharField(default='Full Course', max_length=200, null=True, blank=True)
    price = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Assets(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(default='background',max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

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