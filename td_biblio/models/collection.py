# -*- coding: utf-8 -*-
class Collection(models.Model):
    """Define a collection of entries"""

    name = models.CharField(_("Name"), max_length=100)
    short_description = models.TextField(_("Short description"), blank=True, null=True)
    entries = models.ManyToManyField("Entry", related_name="collections")

    class Meta:
        verbose_name = _("Collection")
        verbose_name_plural = _("Collections")

    def __str__(self):
        return self.name