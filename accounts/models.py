from datetime import datetime,timedelta
from decimal import *
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum, Q
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from accounts.modelmanager import DepartmentManager
from django_countries.fields import CountryField
from accounts.choices import CategoryChoices,SubCategoryChoices

# Create your models here.
class CustomerUser(AbstractUser):
    def get_category_display_name(self):
        return dict(CategoryChoices.choices).get(self.category, 'Unknown')    

    class Score(models.IntegerChoices):
        Male = 1
        Female = 2
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=255)
    phone = models.CharField(default="90001",max_length=255)
    zipcode = models.CharField(blank=True, null=True, max_length=255)
    country = CountryField(blank=True, null=True)
    category = models.IntegerField(choices=CategoryChoices.choices, default=999)
  
    is_admin = models.BooleanField("Is admin", default=False)

    is_active = models.BooleanField('Is active', default=True)
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
    
    def get_login_days(self):
        login_history = LoginHistory.objects.filter(user=self).order_by('login_time')
        return [entry.login_time for entry in login_history]

    def get_login_count(self):
        return LoginHistory.objects.filter(user=self).count()

    def has_logged_in_last_days(self, days):
        recent_date = timezone.now().date() - timedelta(days=days)
        return LoginHistory.objects.filter(user=self, login_time__gte=recent_date).exists()
 

class LoginHistory(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    # You can add more fields as needed

    def __str__(self):
        return f'{self.user.username} - {self.login_time} to {self.logout_time}'

    @property
    def login_duration(self):
        number_hours=(self.logout_time-self.login_time ).hours
        return number_hours
    
class Department(models.Model):
    """Department Table will provide a list of the different departments in CODA"""

    # Department
    # BASIC = "Basic"
    HR = "HR Department"
    IT = "IT Department"
    MKT = "Marketing Department"
    FIN = "Finance Department"
    SECURITY = "Security Department"
    MANAGEMENT = "Management Department"
    # Project = "Project"
    HEALTH = "Health Department"
    Other = "Other"
    DEPARTMENT_CHOICES = [
        # (BASIC, "BASIC Department"),
        (HR, "HR Department"),
        (IT, "IT Department"),
        (MKT, "Marketing Department"),
        (FIN, "Finance Department"),
        # (Project, "Project"),
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
 
# =========================CREDENTIALS TABLE======================================
class CredentialCategory(models.Model):
    department = models.ForeignKey(
        to=Department, on_delete=models.CASCADE, default=Department.get_default_pk
    )
    # created_by= models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("category safe URL"), max_length=255, unique=True
    )
    description = models.TextField(max_length=1000, default=None)
    entry_date = models.DateTimeField(_("entered on"), auto_now_add=True, editable=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("management:credentialcategorylist", args=[self.slug])

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        # return f"{self.category} Categories"
        return f"{self.category}"


class Credential(models.Model):
    USER_CHOICES = [
        ("Superuser", "Superuser"),
        ("Admin", "Admin"),
        ("Employee", "Employee"),
        ("Other", "Other"),
    ]
    category = models.ManyToManyField(
        CredentialCategory, blank=True, related_name="credentialcategory"
    )
    added_by = models.ForeignKey(CustomerUser, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("credential Name"),
        help_text=_("Required"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("credential safe URL"), max_length=255, unique=True
    )
    description = models.TextField(max_length=1000, default=None)
    link_name = models.CharField(max_length=255, default="General")
    link = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(
        max_length=255, blank=True, null=True, default="No Password Needed"
    )
    entry_date = models.DateTimeField(_("entered on"), auto_now_add=True, editable=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    user_types = models.CharField(
        max_length=25,
        choices=USER_CHOICES,
        default="Other",
    )

    class Meta:
        verbose_name_plural = "credentials"

    def get_absolute_url(self):
        return reverse("management:credential")

    def __str__(self):
        return self.name


# ========================================SLUGS GENERATOR====================================================
def credentialcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(credentialcategory_pre_save_receiver, sender=CredentialCategory)


class TaskGroups(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=55,
        unique=True,
        default="Group A"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # @classmethod
    # def get_default_pk(cls):
    #     cat, created = cls.objects.get_or_create(
    #         title="Group A"
    #     )
    #     return cat.pk

    def __str__(self):
        return self.title
# ========================================TIME TRACKER====================================================
# Time Tracking Model
class Tracker(models.Model):
    class Duration(models.IntegerChoices):
        One_Hour = 1
        Two_Hours = 2
        Three_Hours = 3
        Four_Hours = 4
        Five_Hours = 5
        Eight_Hours = 8
        Ten_Hours = 10

    # class AssignedTime(models.IntegerChoices):
    # Plan_A =30
    # Plan_B =120
    # Other = 999

    # Job Category.
    CAT_CHOICES = [
        ("Job_Support", "Job_Support"),
        ("Interview", "Interview"),
        ("Training", "Training"),
        ("Mentorship", "Mentorship"),
        ("Other", "Other"),
    ]
    # Sub Category.
    SUBCAT_CHOICES = [
        ("Requirements", "Requirements"),
        ("Troubleshooting", "Troubleshooting"),
        ("Development", "Development"),
        ("Testing", "Testing"),
        ("Other", "Other"),
    ]
    # Task/Activities
    TASK_CHOICES = [
        ("reporting", "reporting"),
        ("database", "database"),
        ("Business Analysis", "Business Analysis"),
        ("Data Cleaning", "Data Cleaning"),
        ("Other", "Other"), 
    ]
    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
    )
    sub_category = models.CharField(
        max_length=25, choices=SUBCAT_CHOICES, default="Other"
    )
    task = models.CharField(
        max_length=25,
        choices=TASK_CHOICES,
    )
    plan = models.CharField(
        verbose_name=_("group"), help_text=_("Required"), max_length=255, default="B"
    )
    empname = models.ForeignKey(
        "accounts.CustomerUser",
        verbose_name=_("Employee"),
        related_name="Employee",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        #  limit_choices_to=Q(is_staff=True)|Q(is_admin=True) | Q(is_superuser=True) and Q(is_active=True),
        limit_choices_to={"is_staff": True, "is_active": True},
    )

    author = models.ForeignKey(
        "accounts.CustomerUser",
        verbose_name=_("Client"),
        related_name="Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_client": True, "is_active": True},
    )
    employee = models.CharField(
        verbose_name="Company/End Client",
        help_text=_("Required"),
        max_length=255,
        default="CODA",
    )
    # clientname = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE, related_name="clientname",limit_choices_to={'is_client': True})
    login_date = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)
    duration = models.IntegerField(choices=Duration.choices, default=2)
    time = models.PositiveIntegerField(
        # max_digits=3,
        help_text=_("Maximum 200"),
        error_messages={
            "name": {" max_length": ("The maximum hours must be between 0 and 199")}
        },
        default=120,
    )

    class Meta:
        ordering = ["login_date"]

    def get_absolute_url(self):
        return reverse("usertime", args=[self.username])

    @property
    def end(self):
        # date_time = datetime.datetime.now() + datetime.timedelta(hours=2)
        date_time = self.login_date + timedelta(hours=0)
        endtime = date_time.strftime("%H:%M")
        return endtime

    @property
    def total_payment(self):
        total = self.duration.objects.aggregate(TOTAL=Sum("duration"))["TOTAL"]
        return total


class Team_Members(models.Model):
    CAT_CHOICES = [
        ("board", "Board Members"),
        ("analytics_team", "Analytics Team"),
        ("future_talent", "Future Talent"),
        ("support_team", "Support Team"),
        ("clients", "Clients"),
        ("other", "other"),
    ]

    category = models.CharField(
        max_length=25,
        choices=CAT_CHOICES,
        default="Other",
    )

    title = models.CharField(max_length=255, default="Project Manager")
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Team Classification"

    def get_absolute_url(self):
        return reverse("main:layout")

    def __str__(self):
        return self.title

