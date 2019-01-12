import factory

from td_biblio.factories.author_entry_rank import AuthorEntryRankFactory
from td_biblio.factories.entry import EntryFactory


class EntryWithAuthorsFactory(EntryFactory):

    author1 = factory.RelatedFactory(AuthorEntryRankFactory, "entry")
    author2 = factory.RelatedFactory(AuthorEntryRankFactory, "entry")
    author3 = factory.RelatedFactory(AuthorEntryRankFactory, "entry")
