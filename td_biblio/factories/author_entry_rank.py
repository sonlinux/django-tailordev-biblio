import factory

from factory.django import DjangoModelFactory

from td_biblio.factories.author import AuthorFactory
from td_biblio.factories.entry import EntryFactory
from td_biblio.models import AuthorEntryRank


class AuthorEntryRankFactory(DjangoModelFactory):

    author = factory.SubFactory(AuthorFactory)
    entry = factory.SubFactory(EntryFactory)
    rank = factory.Iterator(range(1, 4), cycle=True)

    class Meta:
        model = AuthorEntryRank
