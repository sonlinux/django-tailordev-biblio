# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractEntity(models.Model):
    """Simple abstract entity"""

    name = models.CharField(_("Name"), max_length=150)
    abbreviation = models.CharField(
        _("Entity abbreviation"),
        max_length=100,
        blank=True,
        help_text=_("e.g. Proc Natl Acad Sci U S A"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
