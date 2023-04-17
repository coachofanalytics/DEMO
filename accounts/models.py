from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class User(AbstractUser):
    #fields/columns:username,password,first_Name,last_Name,date_joined,email,is_staff
    class Score(models.IntegerChoices):
        Male = 1
        Female = 2
    gender = models.IntegerField(choices=Score.choices,default=1)
    phone = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField("Is admin", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)


class UserCategory(models.Model):
    # added this column here
    class Category(models.IntegerChoices):
        DYC = 1
        Other = 2
    # added this column here
    class SubCategory(models.IntegerChoices):
        No_selection = 0
        DYC_Business = 1
        DYC_Staff = 2
        DYC_Student = 3
        Other = 4
    user= models.ForeignKey(
        "accounts.User",
        verbose_name=("UserCategories"),
        related_name="UserCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    category = models.IntegerField(choices=Category.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategory.choices, blank=True, null=True
    )
    entry_date = models.DateTimeField("entered on", auto_now_add=True, editable=True)
    class Meta:
        ordering = ["-entry_date"]


class Location(models.Model):
    user= models.ForeignKey(
        "accounts.User",
        verbose_name=("Locations"),
        related_name="Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    address = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    country = CountryField(blank=True, null=True)

class CustomUser(models.Model):
    pass

class UserProfile(models.Model):
    pass


class Department(models.Model):
    pass