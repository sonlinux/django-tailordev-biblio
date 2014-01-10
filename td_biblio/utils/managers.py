# -*- coding: utf-8 -*-
"""
Bibliography Manager Tools
"""
import datetime
import logging

from bibtexparser import customization as bp_customization
from bibtexparser.bparser import BibTexParser
from bibtexparser.latexenc import string_to_latex

from ..models import Author, Journal, Entry, AuthorEntryRank


logger = logging.getLogger('td_biblio')


def to_latex(record):
    """
    Convert strings to latex
    """
    for val in record:
        record[val] = string_to_latex(record[val])
    return record


def td_biblio_customization(record):
    """
    Customize BibTex records parsing
    """
    # Convert crapy things to latex
    record = to_latex(record)
    # and then to unicode
    record = bp_customization.convert_to_unicode(record)
    record = bp_customization.type(record)
    record = bp_customization.author(record)
    record = bp_customization.editor(record)
    record = bp_customization.page_double_hyphen(record)

    return record


def bibtex_import(bibfile):
    """
    Import a bibtex (.bib) bibliography file
    """
    logger.info(u"BibTex import: %s" % bibfile)
    simple_fields = ('type', 'title', 'volume', 'number', 'pages', 'url')
    date_fields = ('day', 'month', 'year')

    with open(bibfile, 'r') as bibfile:

        # Parse BibTex file
        bp = BibTexParser(bibfile, customization=td_biblio_customization)

        # Import each entry
        for bib_item in bp.get_entry_list():

            logger.debug(u"BibTex entry: %s", bib_item)

            # Simple fields
            fields = dict((k, v) for (k, v) in bib_item.iteritems() if k in simple_fields)  # NOPEP8

            # Publication date
            publication_date = {'day': 1, 'month': 1, 'year': 1900}
            publication_date.update(dict((k, int(v)) for (k, v) in bib_item.iteritems() if k in date_fields))  # NOPEP8
            fields['publication_date'] = datetime.date(**publication_date)

            # Foreign keys
            journal, _ = Journal.objects.get_or_create(name=bib_item['journal'])  # NOPEP8
            fields['journal'] = journal

            logger.debug(u"Fields: %s", fields)

            # Save or Update this entry
            entry, _ = Entry.objects.get_or_create(**fields)
            logger.debug(u"Entry: %s", entry)

            # Authors
            for rank, author in enumerate(bib_item['author']):
                last_name, first_name = author.split(', ')

                author, _ = Author.objects.get_or_create(
                    first_name=first_name,
                    last_name=last_name)

                AuthorEntryRank.objects.get_or_create(
                    entry=entry,
                    author=author,
                    rank=rank)