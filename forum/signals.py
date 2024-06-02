# signals.py
import re
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Post, Notification


@receiver(post_save, sender=Post)
def create_mention_notification(sender, instance, created, **kwargs):
    if created:
        mentions = re.findall(r"@(\w+)", instance.content)
        mentioned_users = User.objects.filter(username__in=mentions)
        for user in mentioned_users:
            Notification.objects.create(
                user=user,
                message=f"{instance.author.username} mentioned you in a post.",
            )
