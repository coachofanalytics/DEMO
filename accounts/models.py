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
        verbose_name=("DYC"),
        related_name="DYCUser",
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
        verbose_name=("DYC"),
        related_name="DYCUser",
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



    # class Employee(models.Model):
    #  first_Name=models.CharField(verbose_name=("First Name"), help_text=("Required "), max_length=1000)
    #  last_Name=models.CharField(verbose_name=("Last Name"), help_text=("Required "), max_length=1000)
    #  email=models.CharField(verbose_name=("Employee Email"), help_text=("Required "), max_length=1000)
    #  contact=models.CharField(verbose_name=("Employee contact"), help_text=("Required "), max_length=20, default=25475893847)
    #  entry_date=models.DateTimeField(verbose_name=_("Date"), auto_now=True,editable=True)
    # gender = models.IntegerField(choices=Score.choices, blank=True, null=True)
     
    #  class meta:
    #       verbose_name=_('Employee')
    #       verbose_name_plural=_('Employees')
     
    #  def _str_(self):
    #     return self.email