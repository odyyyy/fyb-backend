from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):
    text = models.CharField(max_length=1024)
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    chat_room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE, related_name='messages')
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']


    def __str__(self):
        return f'{self.sender}: {self.text}'


class ChatRoom(models.Model):
    initiator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='initiated_rooms')
    receiver = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_rooms')

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.initiator.username} -> {self.receiver.username} ({self.created_at})'