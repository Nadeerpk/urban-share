import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import CustomUser
from .models import MessageThread, Message
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.thread_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope["user"].id

        # Save to DB
        await self.save_message(sender_id, self.thread_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @sync_to_async
    def save_message(self, sender_id, thread_id, content):
        sender = CustomUser.objects.get(id=sender_id)
        thread = MessageThread.objects.get(id=thread_id)
        Message.objects.create(thread=thread, sender=sender, content=content)
