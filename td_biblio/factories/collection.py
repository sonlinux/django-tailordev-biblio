import factory
from factory.django import DjangoModelFactory

from td_biblio.models import Collection


class CollectionFactory(DjangoModelFactory):

    name = factory.Sequence(lambda n: "Collection name %s" % n)
    short_description = factory.fuzzy.FuzzyText(length=42)

    class Meta:
        model = Collection

    # m2m
    @factory.post_generation
    def entries(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for entry in extracted:
                self.entries.add(entry)
