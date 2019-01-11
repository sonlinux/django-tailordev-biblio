# -*- coding: utf-8 -*-
from td_biblio.models.abstract_entity import AbstractEntity


class Journal(AbstractEntity):
    """Peer reviewed journal"""

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")