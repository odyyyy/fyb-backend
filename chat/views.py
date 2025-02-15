from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import ChatRoom
from chat.serializers import ChatSerializer, MessageChatRoomSerializer


class ChatView(APIView):

    def get(self, request):
        if 'n' not in request.GET.keys():
            chat_rooms = ChatRoom.objects.filter(Q(initiator_id=request.user.id) |
                                                 Q(receiver_id=request.user.id))
            serializer = ChatSerializer(chat_rooms, many=True, context={'user': request.user})
            return Response(serializer.data)

        chat_room_id = request.GET['n']
        chat_room_data = ChatRoom.objects.filter(Q(pk=chat_room_id) &
                                                 (Q(initiator=request.user) | Q(receiver=request.user)))
        if not chat_room_data.exists():
            return Response({'message': 'No such chatroom'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageChatRoomSerializer(chat_room_data[0])
        return Response(serializer.data)


def chat_test_with_template(request):
    chat_room_id = int(request.GET['n'])

    chat_room_data = ChatRoom.objects.filter(Q(pk=chat_room_id) &
                                             (Q(initiator=request.user) | Q(receiver=request.user)))
    if not chat_room_data.exists():
        raise Http404

    return render(request, 'chat.html',
                  context={'room_name': chat_room_id})
