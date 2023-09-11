from parser.models import ParseTask

import factory
from factory.django import DjangoModelFactory

from accounts.tests.factories.user import UserFactory


class ParseTaskFactory(DjangoModelFactory):
    class Meta:
        model = ParseTask
        django_get_or_create = ("name",)

    name = factory.Faker("name")
    author = factory.SubFactory(UserFactory)
    work_mode = 1
