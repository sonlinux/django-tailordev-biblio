# -*- coding: utf-8 -*-
from td_biblio.models.author import Author
from td_biblio.models.entry import Entry


class AuthorEntryRank(models.Model):
    """Give the author rank for an entry author sequence"""

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    rank = models.IntegerField(
        _("Rank"), help_text=_("Author rank in entry authors sequence")
    )

    class Meta:
        verbose_name = _("Author Entry Rank")
        verbose_name_plural = _("Author Entry Ranks")
        ordering = ("rank",)

    def __str__(self):
        return "%(author)s:%(rank)d:%(entry)s" % {
            "author": self.author,
            "entry": self.entry,
            "rank": self.rank,
        }