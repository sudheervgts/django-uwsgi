
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User

from .background_runs import log_user_changes

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not created:
        log_user_changes(user_obj=instance)
