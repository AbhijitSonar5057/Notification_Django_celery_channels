from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json
from user_app.tasks import get_data
from user_app.models import BroadcastNotification
from notify_user.celery import app as celery_app
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=BroadcastNotification)
# @celery_app.on_after_finalize.connect
def notification_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notification_broadcast",
            {
                'type': 'send_notification',
                'message': json.dumps(str(instance.message))
            }
        # get_data(instance)
        )
        # print("~~~~~~~~~~~~",instance.message,instance.broadcast_on.hour,instance.broadcast_on.minute,instance.broadcast_on.day,instance.broadcast_on.month)
        # schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        # task=PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="user_app.tasks.broadcast_notification", args=json.dumps((instance.id,)))
        # task.save()
        
        
