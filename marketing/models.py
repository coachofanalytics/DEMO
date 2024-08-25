from django.db import models
from main.models import Assets
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from random import randint
# # Create your models here.
from django.contrib.auth import get_user_model
# from finance.utils import get_exchange_rate
User = get_user_model() 
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Ads(models.Model):
    my_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    ad_title = models.CharField(max_length=100, null=True, blank=True)
    bulletin = models.CharField(max_length=100, null=True, blank=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    company_site = models.CharField(max_length=255, null=True, blank=True)
    meeting_link = models.CharField(max_length=500, null=True, blank=True)
    video_link = models.CharField(max_length=500, null=True, blank=True)
    signature = models.CharField(max_length=255, null=True, blank=True)
    description= models.TextField(null=True, blank=True)
    message= models.TextField(null=True, blank=True)
    image_name = models.ForeignKey(
        Assets, related_name="message_image", on_delete=models.CASCADE,default=1,null=True, blank=True
    )
    link = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    #in future we required field that help us to define which platform this ads coming

    def __str__(self):
        return str(self.ad_title)


class Whatsapp_Groups(models.Model):
    # types
    CATEGORY_CHOICES = [
        ("Finance", "Finance"),
        ("IT", "IT"),
        ("Internal", "Internal"),
        ("Political", "Political"),
        ("Business", "Business"),
        ("other", "other"),
    ]
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("data_analysis", "data_analysis"),
        ("coda", "coda"),
        ("Job_Support", "Job_Support"),
        ("interview", "interview"),
        ("mentorship", "mentorship"),
        ("automation", "automation"),
        ("other", "other"),
    ]
    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True,unique=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(
        max_length=25,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="other",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name

# @receiver(pre_save, sender=Whatsapp_Groups)
# def populate_slug(sender, instance, **kwargs):
#     # If the slug is not already set and group_id is present, set the slug based on group_id
#     if not instance.slug and instance.group_id:
#         instance.slug = slugify(instance.group_id)+ str(random(20))

# @receiver(pre_save, sender=Whatsapp_Groups)
# def populate_slug(sender, instance, **kwargs):
#     if not instance.slug and instance.group_id:
#         # Generate a random number between 0 and 99999
#         random_number = randint(0, 99999)
#         # Append the random number to the slugified group_id
#         instance.slug = slugify(instance.group_id) + str(random_number)



@receiver(pre_save, sender=Whatsapp_Groups)
def populate_slug(sender, instance, **kwargs):
    if instance.pk is None and not instance.slug and instance.group_id:
        base_slug = slugify(instance.group_id)
        slug = base_slug
        random_number = randint(0, 9999999)

        # Check if the slug is unique and modify it until it is unique
        while Whatsapp_Groups.objects.filter(slug=slug).exists():
            random_number = randint(0, 9999999)
            slug = f'{base_slug}{random_number}'

        instance.slug = slug


class Whatsapp_dev(TimeStampedModel):
    # types
    CATEGORY_CHOICES = [
        ("Finance", "Finance"),
        ("IT", "IT"),
        ("Internal", "Internal"),
        ("Political", "Political"),
        ("Business", "Business"),
        ("other", "other"),
    ]
    TYPE_CHOICES = [
        ("investments", "investments"),
        ("data_analysis", "data_analysis"),
        ("coda", "coda"),
        ("Job_Support", "Job_Support"),
        ("interview", "interview"),
        ("mentorship", "mentorship"),
        ("other", "other"),
    ]
    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True,unique=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    participants = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(
        max_length=25,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    type = models.CharField(
        max_length=25,
        choices=TYPE_CHOICES,
        default="other",
    )
    # created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # is_active = models.BooleanField(default=False)
    # is_featured = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name
class ReplyMail(models.Model):
	id = models.CharField(max_length=30, unique=True, primary_key=True)
	from_mail = models.CharField(max_length=255)
	to_mail = models.CharField(max_length=255)
	subject = models.CharField(max_length=255)
	text_mail = models.TextField()
	received_date = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "ReplyMail"

	def __str__(self):
		return self.subject
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Email(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='emails')

    def __str__(self):
        return self.subject