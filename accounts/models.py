from django.utils import timezone
from datetime import datetime,timedelta
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from accounts.choices import CategoryChoices, SubCategoryChoices
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
    

class CustomerUser(AbstractUser):
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    def get_category_display_name(self):
        return dict(CategoryChoices.choices).get(self.category, 'Unknown')    

    # added this column here
    def get_subcategory_display_name(self):
        return dict(SubCategoryChoices.choices).get(self.subcategory, 'Unknown')    

    class Score(models.IntegerChoices):
        Male = 1
        Female = 2
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=255)
    gender = models.IntegerField(choices=Score.choices, blank=True, null=True)
    phone = models.CharField(default="90001",max_length=255)
    address = models.CharField(blank=True, null=True, max_length=255)
    city = models.CharField(blank=True, null=True, max_length=255)
    state = models.CharField(blank=True, null=True, max_length=255)
    zipcode = models.CharField(blank=True, null=True, max_length=255)
    country = CountryField(blank=True, null=True)
    category = models.IntegerField(choices=CategoryChoices.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategoryChoices.choices, blank=True, null=True
    )
    is_admin = models.BooleanField("Is admin", default=False)
    is_staff = models.BooleanField("Is employee", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    # is_employee = models.BooleanField("Is employee", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)
    resume_file = models.FileField(upload_to="resumes/doc/", blank=True, null=True)

    # is_active = models.BooleanField('Is applicant', default=True)
    class Meta:
        # ordering = ["-date_joined"]
        ordering = ["username"]
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        fullname = f'{self.first_name},{self.last_name}'
        return fullname
    
    @property
    def user_details(self):
        user_details = (
            f"Username: {self.username}\n"
            f"Phone Number: {self.phone}\n"
            f"Email: {self.email}\n"
            f"City: {self.city}\n"
            # f"Country: {self.country.name if self.country else 'N/A'}"
        )
        return user_details
    
    @property
    def is_recent(self):
        return self.date_joined >= timezone.now() - timedelta(days=365)
    
    @property
    def tenure(self):
        number_days=(timezone.now().date() - self.date_joined.date()).days
        months=number_days/30
        return months
    
  

    