from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView


class ApiUrlsTests(SimpleTestCase):

    def test_get_customers_is_resolved(self):
        url = reverse('login_url')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)
