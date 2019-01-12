from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


PMID_REGEX = r"^-?\d+\Z"
pmid_validator = RegexValidator(
    PMID_REGEX, _("One (or more) PMID is not valid"), "invalid"
)
