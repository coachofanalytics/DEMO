from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import LoginHistory

@receiver(user_logged_in)
def track_login(sender, user, request, **kwargs):
    LoginHistory.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def track_logout(sender, user, request, **kwargs):
    last_login_entry = LoginHistory.objects.filter(user=user).order_by('-login_time').first()
    if last_login_entry and last_login_entry.logout_time is None:
        last_login_entry.logout_time = timezone.now()
        last_login_entry.save()
        
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()



