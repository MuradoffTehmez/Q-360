import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{self.user.id}"

            # Join user notification group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave user notification group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        action = text_data_json.get('action', '')

        # Handle different actions
        if action == 'read_notification':
            notification_id = text_data_json.get('notification_id')
            # Handle marking notification as read
            await self.mark_notification_as_read(notification_id)

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'timestamp': timezone.now().isoformat()
        }))

    async def mark_notification_as_read(self, notification_id):
        # This would update the notification status in the database
        # Implementation would depend on the Notification model
        pass