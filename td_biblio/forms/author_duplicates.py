from django import forms
from django.utils.translation import ugettext_lazy as _
from td_biblio.models import Author


class AuthorDuplicatesForm(forms.Form):
    def get_authors_choices():
        return Author.objects.values_list("id", "last_name")

    authors = forms.MultipleChoiceField(
        label=_("Authors pool"),
        help_text=_("Authors to merge"),
        choices=get_authors_choices,
    )

    alias = forms.ChoiceField(
        label=_("Target author"),
        help_text=_("Reference author for which we will define aliases"),
        choices=get_authors_choices,
    )

    def clean_authors(self):
        authors = self.cleaned_data["authors"]
        return Author.objects.filter(id__in=authors)

    def clean_alias(self):
        alias = self.cleaned_data["alias"]
        return Author.objects.get(id=alias)

    def clean(self):
        super(AuthorDuplicatesForm, self).clean()

        authors = self.cleaned_data.get("authors", [])
        alias = self.cleaned_data.get("alias", None)

        if alias in authors:
            raise forms.ValidationError(
                _("Target author cannot be part of the selection")
            )
