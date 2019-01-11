from django import forms
from django.utils.translation import ugettext_lazy as _
from td_biblio.utils.doi_validator import doi_validator
from td_biblio.utils.pmid_validator import pmid_validator
from td_biblio.utils.text_to_list import text_to_list


class EntryBatchImportForm(forms.Form):

    pmids = forms.CharField(
        label=_("PMID"),
        widget=forms.Textarea(attrs={"placeholder": "ex: 26588162, 19569182"}),
        help_text=_(
            "Paste a list of PubMed Identifiers " "(comma separated or one per line)"
        ),
        required=False,
    )

    dois = forms.CharField(
        label=_("DOI"),
        widget=forms.Textarea(
            attrs={"placeholder": "ex: 10.1093/nar/gks419, 10.1093/nar/gkp323"}
        ),
        help_text=_(
            "Paste a list of Digital Object Identifiers "
            "(comma separated or one per line)"
        ),
        required=False,
    )

    def clean_pmids(self):
        """Transform raw data in a PMID list"""
        pmids = text_to_list(self.cleaned_data["pmids"])
        for pmid in pmids:
            pmid_validator(pmid)
        return pmids

    def clean_dois(self):
        """Transform raw data in a DOI list"""
        dois = text_to_list(self.cleaned_data["dois"])
        for doi in dois:
            doi_validator(doi)
        return dois

    def clean(self):
        super(EntryBatchImportForm, self).clean()

        dois = self.cleaned_data.get("dois", [])
        pmids = self.cleaned_data.get("pmids", [])

        if not len(dois) and not len(pmids):
            raise forms.ValidationError(
                _("You need to submit at least one valid DOI or PMID")
            )
