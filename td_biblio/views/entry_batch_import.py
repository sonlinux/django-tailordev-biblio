import logging

from django.contrib import messages

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.urls import reverse_lazy

from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _

from td_biblio.utils.loaders import DOILoader, PubmedLoader
from td_biblio.exceptions import PMIDLoaderError, DOILoaderError
from td_biblio.forms.entry_batch_import import EntryBatchImportForm
from td_biblio.views.mixins import LoginRequiredMixin, SuperuserRequiredMixin

logger = logging.getLogger("td_biblio")


class EntryBatchImportView(LoginRequiredMixin, SuperuserRequiredMixin, FormView):

    form_class = EntryBatchImportForm
    template_name = "td_biblio/entry_import.html"
    success_url = reverse_lazy("td_biblio:entry_list")

    def form_valid(self, form):
        """Save to database"""
        # PMIDs
        pmids = form.cleaned_data["pmids"]
        if len(pmids):
            pm_loader = PubmedLoader()

            try:
                pm_loader.load_records(PMIDs=pmids)
            except PMIDLoaderError as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            pm_loader.save_records()

        # DOIs
        dois = form.cleaned_data["dois"]
        if len(dois):
            doi_loader = DOILoader()

            try:
                doi_loader.load_records(DOIs=dois)
            except DOILoaderError as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            doi_loader.save_records()

        messages.success(
            self.request,
            _("We have successfully imported {} reference(s).").format(
                len(dois) + len(pmids)
            ),
        )

        return super(EntryBatchImportView, self).form_valid(form)