from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from users.serializers import UserProfileSerializer


class UsersViewsTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user123', email='test_user_email123@mail.com')
        self.client.force_login(self.user)

    def test_user_profile_view_retrieve(self):
        response = self.client.get(reverse('users-profile'))
        serializer = UserProfileSerializer(self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer.data, response.data)

    def test_user_profile_view_update(self):
        response = self.client.patch(reverse('users-profile'), {'username': 'test_user_new_name'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test_user_new_name')
        self.assertEqual(get_user_model().objects.get(id=self.user.id).username, 'test_user_new_name')

    def test_user_profile_view_update_email_not_changed(self):
        response = self.client.patch(reverse('users-profile'), {'email': 'test_user_new_email@mail.com'}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.get(id=self.user.id).email, 'test_user_email123@mail.com')