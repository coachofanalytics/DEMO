from django.db import models
from django.urls import reverse
from django.utils import timezone
from main.models import Assets
from django.contrib.auth import get_user_model
# User=settings.AUTH_USER_MODEL
User = get_user_model()

class Post(models.Model):
    asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codablog:post-detail', kwargs={'pk': self.pk})
    
class Testimonials(models.Model):
    # asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)
    writer = models.ForeignKey(
        User,
        verbose_name=("writer name"),
        on_delete=models.CASCADE,
        # related_name="employee_name"
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('codablog:post-detail', kwargs={'pk': self.pk})

class Rate(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

    def get_absolute_url(self):
        return reverse('codablog:post-detail', kwargs={'pk': self.pk})


class Rated(models.Model):
    class Score(models.IntegerChoices):
        very_Poor = 1
        Poor =2
        Good = 3
        Very_good = 4
        Excellent = 5
    id = models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    topic=models.CharField(max_length=100,default=None)
    rating_date = models.DateTimeField(default=timezone.now)
    punctuality = models.IntegerField(choices=Score.choices)
    communication = models.IntegerField(choices=Score.choices)
    understanding = models.IntegerField(choices=Score.choices)
    rater = models.ForeignKey('accounts.CustomerUser', on_delete=models.CASCADE,default=None)

    class Meta:
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return self.id
'''  
    def get_absolute_url(self):
        return reverse('-detail', kwargs={'pk': self.pk})
'''

