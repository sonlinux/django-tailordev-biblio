import datetime
import factory

from factory.django import DjangoModelFactory

from td_biblio.factories.fuzzy_pages_attribute import FuzzyPages
from td_biblio.factories.journal import JournalFactory
from td_biblio.models import Entry


ENTRY_TYPES_RAW_CHOICES = [c[0] for c in Entry.ENTRY_TYPES_CHOICES]

class EntryFactory(DjangoModelFactory):

    type = factory.fuzzy.FuzzyChoice(ENTRY_TYPES_RAW_CHOICES)
    title = factory.Sequence(lambda n: "Entry title %s" % n)
    journal = factory.SubFactory(JournalFactory)
    publication_date = factory.fuzzy.FuzzyDate(datetime.date(1942, 1, 1))
    volume = factory.fuzzy.FuzzyInteger(1, 10)
    number = factory.fuzzy.FuzzyInteger(1, 50)
    pages = FuzzyPages(1, 2000)

    class Meta:
        model = Entry
