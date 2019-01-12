from td_biblio.factories.abstract_entity import AbstractEntityFactory
from td_biblio.models import Publisher


class PublisherFactory(AbstractEntityFactory):
    class Meta:
        model = Publisher
