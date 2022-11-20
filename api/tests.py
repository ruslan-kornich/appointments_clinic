from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TestCaseBase(APITestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_user(

            username='admin_1', password='admin_1', is_superuser=True
        )

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}


class CategoriesTestClass(TestCaseBase):
    url = reverse('api:workers-list')

    def test_get_list_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    def test_get_list(self):
        response = self.client.get(self.url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
