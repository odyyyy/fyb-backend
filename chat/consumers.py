import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from chat.models import Message, ChatRoom


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_num']




        if ((self.scope['user'].is_anonymous or
             not self.scope['user'].is_authenticated) or
                not await self.is_user_in_room()):

            await self.close()


        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive_json(self, text_data):
        await self.save_message(text_data['message'])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data,
            }
        )

    async def chat_message(self, event):
        message = event['message']['message']
        sender = event['message']['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def save_message(self, message):
        Message.objects.create(text=message,
                               sender=self.scope['user'],
                               chat_room_id=self.room_name)

    @sync_to_async
    def is_user_in_room(self):
        return (ChatRoom.objects.filter(Q(pk=self.room_name) &
                                        (Q(initiator=self.scope['user']) | Q(receiver=self.scope['user'])))
                .exists())
