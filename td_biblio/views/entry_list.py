import datetime
import logging

from django.views.generic import ListView

from td_biblio.models.author import Author
from td_biblio.models.entry import Entry
from td_biblio.models.journal import Journal
from td_biblio.models.collection import Collection

logger = logging.getLogger("td_biblio")


class EntryListView(ListView):
    """Entry list view"""

    model = Entry
    paginate_by = 20
    template = "td_biblio/entry_list.html"

    def get(self, request, *args, **kwargs):
        """Check GET request parameters validity and store them"""

        # -- Publication year
        year = self.request.GET.get("year", None)
        if year is not None:
            try:
                year = datetime.date(int(year), 1, 1)
            except ValueError:
                year = None
        self.current_publication_date = year

        # -- Publication author
        author = self.request.GET.get("author", None)
        if author is not None:
            try:
                author = int(author)
            except ValueError:
                author = None
        self.current_publication_author = author

        # -- Publication collection
        collection = self.request.GET.get("collection", None)
        if collection is not None:
            try:
                collection = int(collection)
            except ValueError:
                collection = None
        self.current_publication_collection = collection

        return super(EntryListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Add GET requests filters
        """
        filters = dict()

        # Publication date
        if self.current_publication_date:
            year = self.current_publication_date.year
            filters["publication_date__year"] = year

        # Publication authors
        if self.current_publication_author:
            author = Author.objects.get(id=self.current_publication_author)
            aliases = list(author.aliases.values_list("id", flat=True))
            filters["authors__id__in"] = [author.id] + aliases

        # Publication collection
        if self.current_publication_collection:
            filters["collections__id"] = self.current_publication_collection

        # Base queryset
        qs = super(EntryListView, self).get_queryset()

        # Return filtered queryset
        return qs.filter(**filters)

    def get_context_data(self, **kwargs):
        """
        Add filtering data to context
        """
        ctx = super(EntryListView, self).get_context_data(**kwargs)

        # -- Metrics
        # Publications (Entries)
        ctx["n_publications_total"] = Entry.objects.count()
        ctx["n_publications_filter"] = self.get_queryset().count()

        # Authors (from selected entries)
        ctx["n_authors_total"] = Author.objects.filter(alias=None).count()
        author_ids = self.get_queryset().values_list("authors__id", flat=True)
        author_ids = list(set(author_ids))
        filtered_authors = Author.objects.filter(id__in=author_ids, alias=None)
        ctx["n_authors_filter"] = filtered_authors.count()

        # Journals (Entries)
        ctx["n_journals_total"] = Journal.objects.count()
        journal_ids = self.get_queryset().values_list("journal__id", flat=True)
        journal_ids = list(set(journal_ids))
        ctx["n_journals_filter"] = len(journal_ids)

        # -- Filters
        # publication date
        ctx["publication_years"] = self.get_queryset().dates(
            "publication_date", "year", order="DESC"
        )
        ctx["current_publication_year"] = self.current_publication_date

        # Publication author
        authors_order = ("last_name", "first_name")
        ctx["publication_authors"] = filtered_authors.order_by(*authors_order)
        ctx["current_publication_author"] = self.current_publication_author

        # Publication collection
        ctx["publication_collections"] = Collection.objects.all()
        ctx[
            "current_publication_collection"
        ] = self.current_publication_collection  # noqa

        return ctx
