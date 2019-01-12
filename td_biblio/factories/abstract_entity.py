from factory.django import DjangoModelFactory
from td_biblio.models import AbstractEntity


class AbstractEntityFactory(DjangoModelFactory):
    class Meta:
        model = AbstractEntity
        abstract = True
