from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

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




