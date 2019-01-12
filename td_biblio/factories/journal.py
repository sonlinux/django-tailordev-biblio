import factory

from td_biblio.factories.abstract_entity import AbstractEntityFactory
from td_biblio.models import Journal


JOURNAL_CHOICES = [
    ("Bioinformatics", "Bioinformatics"),
    ("BMC Bioinf.", "BMC Bioinformatics"),
    ("JACS", "Journal of the American Chemical Society"),
    ("J. Comput. Chem.", "Journal of Computational Chemistry"),
    ("Nat. Biotechnol.", "Nature Biotechnology"),
    ("Nucleic Acids Res.", "Nucleic Acids Research"),
    (
        "PNAS",
        "Proceedings of the National Academy of Sciences of the United "
        "States of America",
    ),
    (
        "Proteins Struct. Funct. Bioinf.",
        "Proteins: Structure, Function, and Bioinformatics",
    ),
]


class JournalFactory(AbstractEntityFactory):

    name = factory.Iterator(JOURNAL_CHOICES, getter=lambda c: c[1])
    abbreviation = factory.Iterator(JOURNAL_CHOICES, getter=lambda c: c[0])

    class Meta:
        model = Journal
        django_get_or_create = ("abbreviation",)
