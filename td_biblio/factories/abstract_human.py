import factory

from factory.django import DjangoModelFactory
from td_biblio.models import AbstractHuman


class AbstractHumanFactory(DjangoModelFactory):

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = AbstractHuman
        abstract = True
