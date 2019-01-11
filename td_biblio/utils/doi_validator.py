from django.core.validators import RegexValidator


DOI_REGEX = r"(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&'<>])\S)+)"

doi_validator = RegexValidator(
    DOI_REGEX, _("One (or more) DOI is not valid"), "invalid"
)
