from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = u'Create a random user'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Number of users created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            User.objects.create_user(username=get_random_string(3),
                                     is_superuser=True,
                                     is_staff=True,
                                     password='1234')
            User.objects.create_user(username=get_random_string(3),
                                     is_staff=True,
                                     password='1234')
            User.objects.create_user(username=get_random_string(3),
                                     password='1234')


