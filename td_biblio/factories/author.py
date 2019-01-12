from td_biblio.factories.abstract_human import AbstractHumanFactory
from td_biblio.models import Author


class AuthorFactory(AbstractHumanFactory):
    class Meta:
        model = Author
