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

class MemberRegistration(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    agree = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"