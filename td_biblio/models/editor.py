# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from td_biblio.models.abstract_human import AbstractHuman


class Editor(AbstractHuman):
    """Journal or book editor"""

    class Meta:
        ordering = ("last_name", "first_name")
        verbose_name = _("Editor")
        verbose_name_plural = _("Editors")
