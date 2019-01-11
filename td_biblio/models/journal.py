# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from td_biblio.models.abstract_entity import AbstractEntity


class Journal(AbstractEntity):
    """Peer reviewed journal"""

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
