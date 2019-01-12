from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


DOI_REGEX = r"(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&'<>])\S)+)"

doi_validator = RegexValidator(
    DOI_REGEX, _("One (or more) DOI is not valid"), "invalid"
)
