import factory

from td_biblio.factories.author_entry_rank import AuthorEntryRankFactory
from td_biblio.factories.entry import EntryFactory


class EntryWithStaticAuthorsFactory(EntryFactory):
    """Fix two authors first and last names"""

    author1 = factory.RelatedFactory(
        AuthorEntryRankFactory,
        "entry",
        author__first_name="John",
        author__last_name="McClane",
        rank=1,
    )

    author2 = factory.RelatedFactory(
        AuthorEntryRankFactory,
        "entry",
        author__first_name="Holly",
        author__last_name="Gennero",
        rank=2,
    )
