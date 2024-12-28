from django.http import JsonResponse
from django.utils.translation import gettext as _
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from bands.models import Band
from bands.permissions import BandLeaderPermission
from bands.serializers import BandSerializer


class BandAPIView(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = BandSerializer
    permission_classes = (IsAuthenticated, BandLeaderPermission)

    def get_object(self):
        return get_object_or_404(Band, leader=self.request.user)

    @extend_schema(
        # Добавление примера ответа в документацию
        request=BandSerializer,
        responses={200: BandSerializer},
        examples=[
            OpenApiExample(
                "Post example",
                description="Test example for the post",
                value=
                {
                    "id": 1,
                    "name": "The Beatles",
                    "city": "Liverpool",
                    "image": "media/photos/bands/2022/01/01/1.jpg",
                    "leader": 1,
                    "members": [1, 2, 3, 4
                                ]
                },
                status_codes=[str(status.HTTP_200_OK)],
            ),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if Band.objects.filter(leader=request.user).exists():
            return JsonResponse({'detail': _('Band already exists')}, status=status.HTTP_400_BAD_REQUEST)
        elif Band.objects.filter(members=request.user).exists():
            return JsonResponse({'detail': _('You are already a member of a band')}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)