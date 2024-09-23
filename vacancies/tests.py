import uuid
from itertools import chain

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from bands.models import Band
from vacancies.models import MusicianVacancy, BandVacancy, OrganizerVacancy

from vacancies.serializers import VacanciesBaseSerializer


class VacanciesTests(TestCase):
    item_uuid = '73680966-8340-4141-affb-32c346f358dd'

    def setUp(self):
        user = get_user_model().objects.create(username='test_user')
        MusicianVacancy.objects.create(created_by=user,
                                       uuid=self.item_uuid,
                                       description='test_description',
                                       instruments=['guitar', 'bass', 'drums'],
                                       level='beginner',
                                       city='London',
                                       contacts=['test_user', 'test_user', 'test_user'],
                                       genres=['Rock', 'Pop', 'jazz'])
        band = Band.objects.create(name='test_band',
                                   leader=user,
                                   city='London',
                                   )
        band.members.set([user])
        BandVacancy.objects.create(created_by=band,
                                   description='test_description',
                                   city='London',
                                   level='beginner',
                                   instrument='guitar',
                                   genres='Rock',
                                   contacts=['test@example', '+79999999931', '@test_user'],)

        OrganizerVacancy.objects.create(created_by=user,
                                        description='test_description',
                                        address='London',
                                        title='test_title',
                                        event_type='concert',
                                        event_datetime='2024-09-18T20:29:50+03:00')

    def test_vacancies_list_view(self):
        response = self.client.get(reverse('vacancies-list'))

        all_vacancies = list(chain(MusicianVacancy.objects.all(),
                                   BandVacancy.objects.all(),
                                   OrganizerVacancy.objects.all()))
        data = VacanciesBaseSerializer(all_vacancies, context={'view_action': 'list'}, many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)

    def test_musician_filter_view(self):
        response = self.client.get(reverse('vacancies-list'), {'q': 'musicians'})
        self.assertEqual(response.status_code, 200)
        data = VacanciesBaseSerializer(MusicianVacancy.objects.all(), context={'view_action': 'list'}, many=True).data
        self.assertEqual(response.data, data)

    def test_band_filter_view(self):
        response = self.client.get(reverse('vacancies-list'), {'q': 'bands'})
        self.assertEqual(response.status_code, 200)
        data = VacanciesBaseSerializer(BandVacancy.objects.all(), context={'view_action': 'list'}, many=True).data
        self.assertEqual(response.data, data)

    def test_organizer_filter_view(self):
        response = self.client.get(reverse('vacancies-list'), {'q': 'organizers'})
        self.assertEqual(response.status_code, 200)
        data = VacanciesBaseSerializer(OrganizerVacancy.objects.all(), context={'view_action': 'list'}, many=True).data
        self.assertEqual(response.data, data)

    def test_vacancies_serializer(self):
        data = VacanciesBaseSerializer(MusicianVacancy.objects.get(uuid=self.item_uuid)).data

        self.assertEqual(data['description'], 'test_description')
        self.assertEqual(data['instruments'], ['guitar', 'bass', 'drums'])
        self.assertEqual(data['level'], 'beginner')
        self.assertEqual(data['city'], 'London')
        self.assertEqual(data['contacts'], ['test_user', 'test_user', 'test_user'])
        self.assertEqual(data['genres'], ['Rock', 'Pop', 'jazz'])

    def test_vacancy_item_view(self):
        response = self.client.get(reverse('vacancies-detail', args=[self.item_uuid]))
        self.assertEqual(response.status_code, 200)
        data = VacanciesBaseSerializer(MusicianVacancy.objects.get(uuid=self.item_uuid)).data
        self.assertEqual(response.data, data)

    def test_vacancy_item_view_not_found(self):
        response = self.client.get(reverse('vacancies-detail', args=['12345678-1234-1234-1234-123456789012']))
        self.assertEqual(response.status_code, 404)
