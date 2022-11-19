from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()




class AuthViewsTests(APITestCase):

    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_current_user(self):
        url = reverse("api:login_url")

        user = User.objects.create_user(username='usuario', email='usuario@mail.com', password='contrasegna')
        self.assertEqual(user.is_active, 1, 'Active User')


        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']

        # Next post/get's will require the token to connect
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(token))
        response = self.client.get(reverse('api:workers-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

class TestCaseBase(APITestCase):
    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_user(

            username='admin_1', password='admin_1', is_superuser=True
        )

        refresh = RefreshToken.for_user(user)
        print(refresh)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}


class CategoriesTestClass(TestCaseBase):
    url = reverse('api:workers-list')
    # def test_post_workers(self):
    #     data = {
    #         "first_name": "Alberto",
    #         "last_name": "McKaylin",
    #         "phone": "+12345678910",
    #         "specialty": "Therapist"
    #
    #     }
    #     response = self.client.post(self.url, data=data, **self.bearer_token)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_no_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.data
        )

    def test_get_list(self):
        response = self.client.get(self.url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


