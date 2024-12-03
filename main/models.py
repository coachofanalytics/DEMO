from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Page(models.Model):
    page_name = models.CharField(max_length=200)

    def __str__(self):
        return self.page_names


class Description(models.Model):
    page = models.ForeignKey(Page, related_name='descriptions', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.name} for {self.page.page_name}"


# Content Model
class Content(models.Model):
    SECTION_CHOICES = [
        ('Our Story', 'Our Story'),
        ('Newsletter', 'Newsletter'),
        ('Blog', 'Blog'),
    ]

    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.section} - {self.title if self.title else 'Content'}"


# Assets Model
class Assets(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(default='background', max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Assets"

    @property
    def split_name(self):
        image_1 = self.name.split("_")[0]
        image_2 = self.name.split("_")[1]
        return image_1, image_2

    def __str__(self):
        return self.name


# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    topic = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.topic  # Corrected to use 'topic'


# Service Model
class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


# SubService Model
class SubService(models.Model):
    service = models.ForeignKey(Service, related_name='subservices', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.service}"


# News Model
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(null=True, blank=True)
    published_date = models.DateField()
    is_event = models.BooleanField(default=False)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)

    def __str__(self):
        return self.title



# class Teams(models.Model):
#     ROLE_CHOICES = [
#         ('Governor', 'Governor'),
#         ('Deputy Governor', 'Deputy Governor'),
#         ('Regional Coordinator', 'Regional Coordinator'),
#         ('Team Member', 'Team Member'),
#     ]

#     LEADERSHIP_CHOICES = [
#         ('Local', 'Local'),
#         ('Global', 'Global'),
#     ]

#     name = models.CharField(max_length=255)
#     leadership = models.CharField(max_length=50, choices=LEADERSHIP_CHOICES, default='Local')
#     facebook_link = models.URLField(blank=True, null=True)
#     linkedin_link = models.URLField(blank=True, null=True)
#     twitter_link = models.URLField(blank=True, null=True)
#     role = models.CharField(max_length=50, choices=ROLE_CHOICES)
#     region = models.CharField(max_length=255, blank=True, null=True)
#     image = models.ImageField(upload_to='people/')
#     bio = models.TextField()

#     def __str__(self):
#         return self.name


# Gallery Model
class Gallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField()

    def __str__(self):
        return self.title


# ContactUs Model
class ContactUs(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the user.")
    email = models.EmailField(help_text="Email address for correspondence.")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, 
        help_text="Phone number of the user (optional)."
    )
    message = models.TextField(help_text="Message or inquiry from the user.")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the message was submitted.")
    is_resolved = models.BooleanField(default=False, help_text="Flag to mark whether the query has been addressed.")

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
