from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Notification


@receiver(post_save, sender=Notification)
def handle_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"user_{instance.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
            }
        )
