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
    
class Plan(models.Model):
    CAT_CHOICES = [
        ("Financial", "Financial"),
        ("Health", "Health"),
        ("Family", "Family"),
        ("Other", "Other"),
    ]
    GOAL_CHOICES = [
        ("Business", "Business"),
        ("Employment", "Employment"),
        ("Savings", "Savings"),
        ("Insurance", "Insurance"),
        ("Trips", "Trips"),
    ]
    STATUS_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default="Other",
    )
    goal = models.CharField(
        max_length=25,
        choices=GOAL_CHOICES,
        default="Other",
    )
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="Low",
    )
    planner = models.ForeignKey(
        User,
        related_name="planner",
        null=True,
        blank=True,
        default=1,
        on_delete=models.SET_NULL,
        limit_choices_to=Q(is_active=True)
        and (Q(is_admin=True) | Q(is_superuser=True)),
    )
    responsible_party = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1,
        limit_choices_to=Q(is_active=True)
        and (Q(is_staff=True) | Q(is_admin=True) | Q(is_superuser=True)),
    )
    task = models.CharField(max_length=255, default="CODA")
    duration = models.IntegerField(null=False, default=4)  # how long will it take
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    what = models.TextField()  # What is needed?
    why = models.TextField()  # Why do they need it ?
    how = (
        models.TextField()
    )  # how should it be delivered/Which platform or mode of delivery?
    comments = models.TextField(default='No Comment',null=True, blank=True)  # What is needed?
    doc = models.FileField(upload_to="Uploads/Support_Docs/", null=True, blank=True)
    pptlink = models.CharField(max_length=300, default="link",null=True, blank=True)
    videolink = models.CharField(max_length=300, default="Video",null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Plan"
        # ordering = ["-created_at","-updated_at"]

    @property
    def doc_url(self):
        if self.doc and hasattr(self.doc, 'url'):
            return self.doc.url
    @property
    def delivery(self):
        delivery=self.duration + self.created_at
        return delivery

    def get_absolute_url(self):
        return reverse("main:plans")

    def __str__(self):
        return self.goal

