# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from td_biblio.models.abstract_entity import AbstractEntity


class Publisher(AbstractEntity):
    """Journal or book publisher"""

    class Meta:
        verbose_name = _("Publisher")
        verbose_name_plural = _("Publishers")
