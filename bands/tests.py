import uuid
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from .models import Band
from .serializers import BandSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import status

class BandTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user', email='test_user_email')
        self.user2 = get_user_model().objects.create(username='test_user2', email='test_user2_email')

        self.band = Band.objects.create(
            name="test_band",
            leader=self.user,
            city="St Petersburg",
            image=None
        )
        self.band.members.set([self.user, self.user2])

        self.bands_endpoint =  reverse('bands:bands')

    def test_band_view_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.bands_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BandSerializer(self.band).data)

    def test_band_view_detail_not_authenticated(self):
        response = self.client.get(self.bands_endpoint)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('Authentication credentials were not provided.')})

    def test_band_view_detail_authenticated_but_not_leader(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.bands_endpoint)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': _('You do not have permission to perform this action.')})



    def test_band_view_create(self):
        new_user = get_user_model().objects.create(username='new_user_not_in_band', email='new_user_not_in_band@mail.com')

        self.client.force_authenticate(user=new_user)
        response = self.client.post(self.bands_endpoint, {
            'name': 'new_band',
            'leader': new_user.pk,
            'city': 'Moscow',
            'members': [new_user.pk],
        }, format='json')

        print('DSADASDLASSA', Band.objects.all())


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Band.objects.count(), 2)
        self.assertEqual(Band.objects.get(name='new_band').leader, new_user)


    def test_band_view_create_not_authenticated(self):
        response = self.client.post(self.bands_endpoint, {
            'name': 'test_band2',
            'leader': self.user2.pk,
            'city': 'Moscow',
            'members': [self.user.pk, self.user2.pk],
        }, format='json')


        self.assertEqual(Band.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_band_view_create_if_user_already_in_band(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.bands_endpoint, {
            'name': 'test_band2',
            'leader': self.user2.pk,
            'city': 'Moscow',
            'members': [self.user.pk, self.user2.pk],
        }, format='json')

        self.assertEqual(Band.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': _('You are already a member of a band')})

    def test_band_view_update(self):
        self.client.force_authenticate(user=self.user)
        band_new_name = 'The New Band'
        response = self.client.patch(self.bands_endpoint, {
            'name': band_new_name,
            'city': 'Moscow',
        }, format='json')

        self.assertEqual(Band.objects.get(name=band_new_name).city, 'Moscow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_band_view_update_not_authenticated(self):
        band_new_name = 'The New Band'
        response = self.client.patch(self.bands_endpoint, {
            'name': band_new_name,
            'city': 'Moscow',
        }, format='json')

        self.assertEqual(Band.objects.get(name=self.band.name).city, 'St Petersburg')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_band_view_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.bands_endpoint)

        self.assertEqual(Band.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)