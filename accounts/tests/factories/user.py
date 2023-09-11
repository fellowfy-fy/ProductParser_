import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    email = factory.Faker("email")
