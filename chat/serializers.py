from rest_framework import serializers

from users.serializers import CompanionUserSerializer
from .models import Message, ChatRoom


class MessageChatRoomSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            'initiator': CompanionUserSerializer(instance.initiator).data,
            'receiver': CompanionUserSerializer(instance.receiver).data,

            'messages': MessageSerializer(instance.messages.all(), many=True).data

        }

        return data


class MessageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['sender'] = instance.sender.username
        return data

    class Meta:
        model = Message
        fields = ('text', 'sent_at', 'sender')


class ChatSerializer(serializers.ModelSerializer):
    chatroom_with_user = serializers.SerializerMethodField()

    def get_chatroom_with_user(self, obj):
        return CompanionUserSerializer(obj.initiator).data \
            if obj.receiver == self.context['user'] else CompanionUserSerializer(obj.receiver).data

    class Meta:
        model = ChatRoom
        fields = ('id', 'created_at', 'chatroom_with_user')
