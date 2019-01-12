import logging

from td_biblio.forms import AuthorDuplicatesForm
from td_biblio.models.author import Author
from td_biblio.views.mixins import LoginRequiredMixin, SuperuserRequiredMixin

from django.contrib import messages

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from django.utils.encoding import force_text

from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView
from django.views.generic.edit import FormMixin

logger = logging.getLogger("td_biblio")


class FindDuplicatedAuthorsView(
    LoginRequiredMixin, SuperuserRequiredMixin, FormMixin, ListView
):

    form_class = AuthorDuplicatesForm
    model = Author
    ordering = ("last_name", "first_name")
    paginate_by = 30
    queryset = Author.objects.filter(alias=None)
    success_url = reverse_lazy("td_biblio:duplicates")
    template_name = "td_biblio/find_duplicated_authors.html"

    def _add_aliases(self, authors, alias):
        return authors.update(alias=alias)

    def form_valid(self, form):

        authors = form.cleaned_data["authors"]
        alias = form.cleaned_data["alias"]
        match = self._add_aliases(authors, alias)

        messages.success(
            self.request,
            _("Added '{}' as alias for {} author(s).").format(
                alias.get_formatted_name(), match
            ),
        )

        return super(FindDuplicatedAuthorsView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        ctx = super(FindDuplicatedAuthorsView, self).get_context_data(**kwargs)
        ctx.update({"paginate_by": self.get_paginate_by(self.queryset)})
        return ctx

    def get_paginate_by(self, queryset):

        by = self.request.GET.get("by", None)
        if not by:
            return self.paginate_by
        try:
            return int(by)
        except ValueError:
            pass

    def get_success_url(self):
        """Add get parameters"""
        url = force_text(self.success_url)
        if self.request.GET:
            url = "{}?{}".format(url, self.request.GET.urlencode())
        return url

    def post(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
