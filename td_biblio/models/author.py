# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from td_biblio.models.abstract_human import AbstractHuman


class Author(AbstractHuman):
    """Entry author"""

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
