from parser.models import SiteParseSettings

import factory
from factory.django import DjangoModelFactory


class SiteParseSettingsFactory(DjangoModelFactory):
    class Meta:
        model = SiteParseSettings
        django_get_or_create = ("url",)

    url = factory.Faker("url")

    path_title = "h2"
    path_price = "span"
