from rest_framework import generics, mixins
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
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = (IsAuthenticated, BandLeaderPermission)

