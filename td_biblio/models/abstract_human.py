# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class AbstractHuman(models.Model):
    """Simple Abstract Human model

    Note that this model may be linked to django registered users
    """

    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    first_initial = models.CharField(_("First Initial(s)"), max_length=10,
                                     blank=True)

    # This is a django user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        on_delete=models.CASCADE
    )

    alias = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="aliases",
        related_query_name="alias_human",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_formatted_name()

    def save(self, *args, **kwargs):
        """Set initials and try to set django user before saving"""

        self._set_first_initial()
        self._set_user()
        super(AbstractHuman, self).save(*args, **kwargs)

    def _set_first_initial(self, force=False):
        """Set author first name initial"""

        if self.first_initial and not force:
            return
        self.first_initial = " ".join([c[0] for c in self.first_name.split()])

    def get_formatted_name(self):
        """Return author formated full name, e.g. Maupetit J"""

        return "%s %s" % (self.last_name, self.first_initial)

    def _set_user(self):
        """Look for local django user based on human name"""

        if "" in (self.last_name, self.first_name):
            return

        self._set_first_initial()

        User = get_user_model()
        try:
            self.user = User.objects.get(
                models.Q(last_name__iexact=self.last_name),
                models.Q(first_name__iexact=self.first_name) | models.Q(
                    first_name__istartswith=self.first_initial[0]),
            )
        except User.DoesNotExist:
            pass
        except User.MultipleObjectsReturned:
            pass
