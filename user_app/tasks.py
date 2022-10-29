from pkgutil import get_data
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from user_app.models import BroadcastNotification
from celery import Celery,states
from celery.exceptions import Ignore
import json
import asyncio


@shared_task(bind=True)
def broadcast_notification(self,data):
    print("-------~~~~~~~~~~~~>>.celery Task......")
    try:
        notication=BroadcastNotification.objects.filter(id=int(data))
        if len(notication)>0:
            notication=notication.first()
            channel_layer = get_channel_layer()
            loop=asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send)(
                "notification_broadcast",
                {
                    'type': 'send_notification',
                    'message': json.dumps(notication.message)
                }
            )
            notication.sent=True
            notication.save()
            return "Done"
        else:
            self.update_state(
                state='FAILURE',
                meta={'exe':"Not Found"}
            )
            raise Ignore()
            
            # async_to_sync(channel_layer.group_send)(
            #     "notification_broadcast",
            #     {
            #         'type': 'send_notification',
            #         'message': json.dumps("Notification")
            #     }
            # )
        
    except Exception as e:
        self.update_state(
                state='FAILURE',
                meta={'exe':"Not Found"}
            )
        raise Ignore()