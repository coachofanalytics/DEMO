from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class User(AbstractUser):
    #fields/columns:username,password,first_Name,last_Name,date_joined,email,is_staff
    class Score(models.IntegerChoices):
        Male = 1
        Female = 2
    gender = models.IntegerField(choices=Score.choices,default=1)
    email = models.EmailField(unique=True)  # Add unique=True to make email field unique
    phone = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField("Is admin", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)

    class meta:
        # ordering = ["username"]
        ordering = ["-date_joined"]

    def __str__(self):
        # return str(self.email)
        return str(self.username)
    
    @property
    def full_name(self):
        full_name=self.first_name +' ' + self.last_name
        return full_name


class VisaService(models.Model):
    class SubCategory(models.IntegerChoices):
        No_selection = 0
        F1 = 1,'STUDENT VISA'
        B1 = 2,'BUSINESS VISA'
        H1 = 3,'WORK VISA'
        GC = 4,'GREEN CARD'
        Asylum = 5,'ASYLUM'
        OTHER = 6,'OTHER'


    name = models.CharField(max_length=254)
    sub_category = models.IntegerField(choices=SubCategory.choices)
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class UserCategory(models.Model):

    class Category(models.IntegerChoices):
        No_selection = 0
        Student = 1,'STUDENT'
        Business = 2,'BUSINESS'
        Residence = 3,'RESIDENCE(GC)'
        Staff = 4,'DYC EMPLOYEE'
        Other = 5,'OTHER'

    class SubCategory(models.IntegerChoices):
        No_selection = 0
        F1 = 1,'STUDENT VISA'
        B1 = 2,'BUSINESS VISA'
        H1 = 3,'WORK VISA'
        GC=4,'GREEN CARD'
        Asylum=5,'ASYLUM'
        OTHER = 6,'OTHER'

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
        verbose_name_plural = "Service Categories"
        ordering = ["-entry_date"]
        unique_together = (("user", "category"),)

    def __str__(self):
        return self.get_category_display()


class Location(models.Model):
    user = models.ForeignKey(
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


class UserProfile(models.Model):
    pass
