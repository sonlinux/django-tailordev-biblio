# -*- coding: utf-8 -*-
class Entry(models.Model):
    """The core model for references

    Largely guided by the BibTeX file format (see
    http://en.wikipedia.org/wiki/BibTeX).

    Unsupported fields (for now):

    * eprint: A specification of an electronic publication, often a preprint
      or a technical report
    * howpublished: How it was published, if the publishing method is
      nonstandard
    * institution: The institution that was involved in the publishing, but not
      necessarily the publisher
    * key: A hidden field used for specifying or overriding the alphabetical
      order of entries (when the "author" and "editor" fields are missing).
      Note that this is very different from the key (mentioned just after this
      list) that is used to cite or cross-reference the entry.
    * series: The series of books the book was published in (e.g. "The Hardy
      Boys" or "Lecture Notes in Computer Science")
    * type: The field overriding the default type of publication (e.g.
      "Research Note" for techreport, "{PhD} dissertation" for phdthesis,
      "Section" for inbook/incollection)
    """

    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    MANUAL = "manual"
    MASTERSTHESIS = "mastersthesis"
    MISC = "misc"
    PHDTHESIS = "phdthesis"
    PROCEEDINGS = "proceedings"
    TECHREPORT = "techreport"
    UNPUBLISHED = "unpublished"

    ENTRY_TYPES_CHOICES = (
        (ARTICLE, _("Article")),
        (BOOK, _("Book")),
        (BOOKLET, _("Book (no publisher)")),
        (CONFERENCE, _("Conference")),
        (INBOOK, _("Book chapter")),
        (INCOLLECTION, _("Book from a collection")),
        (INPROCEEDINGS, _("Conference proceedings article")),
        (MANUAL, _("Technical documentation")),
        (MASTERSTHESIS, _("Master's Thesis")),
        (MISC, _("Miscellaneous")),
        (PHDTHESIS, _("PhD Thesis")),
        (PROCEEDINGS, _("Conference proceedings")),
        (TECHREPORT, _("Technical report")),
        (UNPUBLISHED, _("Unpublished work")),
    )

    type = models.CharField(
        _("Entry type"), max_length=50, choices=ENTRY_TYPES_CHOICES, default=ARTICLE
    )

    # Base fields
    title = models.CharField(_("Title"), max_length=255)
    authors = models.ManyToManyField(
        "Author", related_name="entries", through="AuthorEntryRank"
    )
    journal = models.ForeignKey(
        "Journal", related_name="entries", blank=True, on_delete=models.CASCADE
    )
    publication_date = models.DateField(_("Publication date"), null=True)
    is_partial_publication_date = models.BooleanField(
        _("Partial publication date?"),
        default=True,
        help_text=_(
            "Check this if the publication date is incomplete (for example "
            "if only the year is valid)"
        ),
    )
    volume = models.CharField(
        _("Volume"),
        max_length=50,
        blank=True,
        help_text=_("The volume of a journal or multi-volume book"),
    )
    number = models.CharField(
        _("Number"),
        max_length=50,
        blank=True,
        help_text=_(
            "The '(issue) number' of a journal, magazine, or tech-report, if "
            "applicable. (Most publications have a 'volume', but no 'number' "
            "field.)"
        ),
    )
    pages = models.CharField(
        _("Pages"),
        max_length=50,
        blank=True,
        help_text=_("Page numbers, separated either by commas or " "double-hyphens"),
    )
    url = models.URLField(
        _("URL"), blank=True, help_text=_("The WWW address where to find this resource")
    )

    # Identifiers
    doi = models.CharField(
        _("DOI"),
        max_length=100,
        blank=True,
        help_text=_("Digital Object Identifier for this resource"),
    )
    issn = models.CharField(
        _("ISSN"),
        max_length=20,
        blank=True,
        help_text=_("International Standard Serial Number"),
    )
    isbn = models.CharField(
        _("ISBN"),
        max_length=20,
        blank=True,
        help_text=_("International Standard Book Number"),
    )
    pmid = models.CharField(
        _("PMID"), blank=True, max_length=20, help_text=_("Pubmed ID")
    )

    # Book
    booktitle = models.CharField(
        _("Book title"),
        max_length=50,
        blank=True,
        help_text=_("The title of the book, if only part of it is being cited"),
    )
    edition = models.CharField(
        _("Edition"),
        max_length=100,
        blank=True,
        help_text=_(
            "The edition of a book, long form (such as 'First' or " "'Second')"
        ),
    )
    chapter = models.CharField(_("Chapter number"), max_length=50, blank=True)

    # PhD Thesis
    school = models.CharField(
        _("School"),
        max_length=50,
        blank=True,
        help_text=_("The school where the thesis was written"),
    )

    # Proceedings
    organization = models.CharField(
        _("Organization"),
        max_length=50,
        blank=True,
        help_text=_("The conference sponsor"),
    )

    # Misc
    editors = models.ManyToManyField("Editor", related_name="entries", blank=True)
    publisher = models.ForeignKey(
        "Publisher",
        related_name="entries",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        _("Address"),
        max_length=250,
        blank=True,
        help_text=_(
            "Publisher's address (usually just the city, but can be the full "
            "address for lesser-known publishers)"
        ),
    )
    annote = models.CharField(
        _("Annote"),
        max_length=250,
        blank=True,
        help_text=_("An annotation for annotated bibliography styles (not typical)"),
    )
    note = models.TextField(
        _("Note"), blank=True, help_text=_("Miscellaneous extra information")
    )

    # Related publications
    crossref = models.ManyToManyField("self", blank=True)

    class Meta:
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        ordering = ("-publication_date",)

    def __str__(self):
        """Format entry with a default bibliography style"""
        # Authors
        author_str = "%(last_name)s %(first_initial)s"
        s = ", ".join([author_str % a.__dict__ for a in self.get_authors()])
        s = ", and ".join(s.rsplit(", ", 1))  # last author case
        s += ", "

        # Title
        s += '"%(title)s", ' % self.__dict__

        # Journal
        if self.journal.abbreviation:
            s += "in %(abbreviation)s, " % self.journal.__dict__
        else:
            # fall back to the real name
            s += "in %(name)s, " % self.journal.__dict__

        # Misc
        if self.volume and self.pages:
            s += "vol. %(volume)s, pp. %(pages)s, " % self.__dict__
        if self.publication_date:
            s += "%s." % self.publication_date.strftime("%B %Y")

        return s

    def _get_first_author(self):
        """
        Get this entry first author
        """
        if not len(self.get_authors()):
            return ""
        return self.get_authors()[0]

    first_author = property(_get_first_author)

    def _get_last_author(self):
        """
        Get this entry last author
        """
        if not len(self.get_authors()):
            return ""
        return self.get_authors()[-1]

    last_author = property(_get_last_author)

    def get_authors(self):
        """
        Get ordered authors list

        Note that authorentryrank_set is ordered as expected while the authors
        queryset is not (M2M with a through case).
        """
        return [aer.author for aer in self.authorentryrank_set.all()]