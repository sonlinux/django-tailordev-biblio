from django.core.validators import RegexValidator

PMID_REGEX = r"^-?\d+\Z"
pmid_validator = RegexValidator(
    PMID_REGEX, _("One (or more) PMID is not valid"), "invalid"
)
