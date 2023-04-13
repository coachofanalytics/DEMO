from datetime import datetime,timedelta
from decimal import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from accounts.modelmanager import DepartmentManager
from django_countries.fields import CountryField

# Create your models here.
class CustomerUser(AbstractUser):
    class Category(models.IntegerChoices):
        Job_Applicant = 1
        Coda_Staff_Member = 2
        Client_OR_Customer_or_Student = 3
        General_User = 4

    # added this column here
    class SubCategory(models.IntegerChoices):
        No_selection = 0
        Job_Support = 1
        Student = 2
        Full_time = 3
        Contractual = 4
        Agent = 5
        DC48Kenya = 6
        DYC = 7
        Other = 8

    class Score(models.IntegerChoices):
        Male = 1
        Female = 2

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=100)
    gender = models.IntegerField(choices=Score.choices, blank=True, null=True)
    phone = models.CharField(default="90001", max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    country = CountryField(blank=True, null=True)
    category = models.IntegerField(choices=Category.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategory.choices, blank=True, null=True
    )
    # category=models.IntegerField(choices=Category.choices,blank=True,null=False)
    # applicant=models.BooleanField('Is Job Applicant', default=True)
    # Changes Made to Model-3/29/2022
    is_admin = models.BooleanField("Is admin", default=False)
    is_employee = models.BooleanField("Is employee", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)
    resume_file = models.FileField(upload_to="resumes/doc/", blank=True, null=True)

    # is_active = models.BooleanField('Is applicant', default=True)
    class Meta:
        # ordering = ["-date_joined"]
        ordering = ["username"]

    @property
    def full_name(self):
        fullname = f'{self.first_name},{self.last_name}'
        return fullname
    
    def is_recent(self):
        return self.date_joined >= timezone.now() - timedelta(days=365)
    
# class CODA_User_Categories(models.model):
#     # added this column here
#     class Category(models.IntegerChoices):
#         Job_Applicant = 1
#         Coda_Staff_Member = 2
#         Client_OR_Customer_or_Student = 3
#         DYC_Business = 4
#         DYC_Staff = 5
#         DYC_Student = 6
#         No_selection = 0
#         Other = 8
#     # added this column here
#     class SubCategory(models.IntegerChoices):
#         No_selection = 0
#         Job_Support = 1
#         Student = 2
#         Full_time = 3
#         Contractual = 4
#         Agent = 5
#         Other = 8
#     user= models.ForeignKey(
#         "accounts.CustomUser",
#         verbose_name=_("User"),
#         related_name="user",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         limit_choices_to={"is_employee": True, "is_active": True},
#     )
#     category = models.IntegerField(choices=Category.choices, default=999)
#     # added this column here
#     sub_category = models.IntegerField(
#         choices=SubCategory.choices, blank=True, null=True
#     )



    

class CustomUser(models.Model):
    class Category(models.IntegerChoices):
        CODA = 1
        DYC=2
        General_User = 3
    class Score(models.IntegerChoices):
        Male = 1
        Female = 2
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=100)
    gender = models.IntegerField(choices=Score.choices, blank=True, null=True)
    phone = models.CharField(default="90001", max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
    city = models.CharField(blank=True, null=True, max_length=100)
    state = models.CharField(blank=True, null=True, max_length=100)
    country = CountryField(blank=True, null=True)
    category = models.IntegerField(choices=Category.choices, default=999)
    # Changes Made to Model-3/29/2022
    is_admin = models.BooleanField("Is admin", default=False)
    is_employee = models.BooleanField("Is employee", default=False)
    is_client = models.BooleanField("Is Client", default=False)
    is_applicant = models.BooleanField("Is applicant", default=False)
    is_employee_contract_signed = models.BooleanField(default=False)
    resume_file = models.FileField(upload_to="resumes/doc/", blank=True, null=True)

    # is_active = models.BooleanField('Is applicant', default=True)
    class Meta:
        # ordering = ["-date_joined"]
        ordering = ["username"]

    @property
    def full_name(self):
        fullname = f'{self.first_name},{self.last_name}'
        return fullname
    
    def is_recent(self):
        return self.date_joined >= timezone.now() - timedelta(days=365)
    

class CODAUserCategories(models.Model):
    # added this column here
    class Category(models.IntegerChoices):
        Job_Applicant = 1
        Coda_Staff_Member = 2
        Client_OR_Customer_or_Student = 3
        No_selection = 0
        Other = 8
    # added this column here
    class SubCategory(models.IntegerChoices):
        No_selection = 0
        Job_Support = 1
        Student = 2
        Full_time = 3
        Contractual = 4
        Agent = 5
        Other = 8
    user= models.ForeignKey(
        "accounts.CustomUser",
        verbose_name=_("User"),
        related_name="user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to=Q(is_employee=True)|Q(is_admin=True) | Q(category=1) and Q(is_active=True)
        # limit_choices_to={"is_employee": True, "category"=1, "is_active": True},
    )
    category = models.IntegerField(choices=Category.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategory.choices, blank=True, null=True
    )
    entry_date = models.DateTimeField(_("entered on"), auto_now_add=True, editable=True)
    class Meta:
        ordering = ["-entry_date"]
        # ordering = ["username"]

class DYCUserCategories(models.Model):
    # added this column here
    class Category(models.IntegerChoices):
        DYC_Business = 4
        DYC_Staff = 5
        DYC_Student = 6
        No_selection = 0
        Other = 8
    # added this column here
    class SubCategory(models.IntegerChoices):
        No_selection = 1
        Agent = 2
        Other = 3
    user= models.ForeignKey(
        "accounts.CustomUser",
        verbose_name=_("DYCUser"),
        related_name="DYCUser",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_employee": True, "is_active": True},
    )
    category = models.IntegerField(choices=Category.choices, default=999)
    # added this column here
    sub_category = models.IntegerField(
        choices=SubCategory.choices, blank=True, null=True
    )
    entry_date = models.DateTimeField(_("entered on"), auto_now_add=True, editable=True)
    class Meta:
        ordering = ["-entry_date"]
        # ordering = ["username"]

        
class Department(models.Model):
    """Department Table will provide a list of the different departments in CODA"""

    # Department
    HR = "HR Department"
    IT = "IT Department"
    MKT = "Marketing Department"
    FIN = "Finance Department"
    SECURITY = "Security Department"
    MANAGEMENT = "Management Department"
    HEALTH = "Health Department"
    Other = "Other"
    DEPARTMENT_CHOICES = [
        (HR, "HR Department"),
        (IT, "IT Department"),
        (MKT, "Marketing Department"),
        (FIN, "Finance Department"),
        (SECURITY, "Security Department"),
        (MANAGEMENT, "Management Department"),
        (HEALTH, "Health Department"),
        (Other, "Other"),
    ]

    name = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
        default=Other,
    )

    description = models.TextField(max_length=500, null=True, blank=True)
    slug = models.SlugField(
        verbose_name=_("Department safe URL"), max_length=255, unique=True
    )
    # created_date = models.DateTimeField(_('entered on'),default=timezone.now, editable=True)
    is_featured = models.BooleanField("Is featured", default=True)
    is_active = models.BooleanField(default=True)

    objects=DepartmentManager()

    @classmethod
    def get_default_pk(cls):
        cat, created = cls.objects.get_or_create(
            name="Other", defaults=dict(description="this is not an cat")
        )
        return cat.pk

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    # def get_absolute_url(self):
    #     return reverse('management:department_list', args=[self.slug])

    def __str__(self):
        return self.name


# ========================================SLUGS GENERATOR====================================================
class UserProfile(models.Model):
    user = models.OneToOneField(
        "accounts.CustomerUser", related_name="profile", on_delete=models.CASCADE
    )
    position = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    image = models.ImageField(
        default="default.jpg", upload_to="Application_Profile_pics", blank=True
    )
    is_active = models.BooleanField("Is featured", default=True)

    def __str__(self):
        return f"{self.user.username} Profile"