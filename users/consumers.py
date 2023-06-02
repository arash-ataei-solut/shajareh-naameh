from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            group_name = f"user_{user.id}"
            await self.channel_layer.group_add(group_name, self.channel_name)

            await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]

        if user.is_authenticated:
            channel_name = f"user_{user.id}"
            await self.channel_layer.group_discard(channel_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data='')
