from django.db import models
from django.utils.translation import gettext_lazy as _


class VerdictType(models.TextChoices):
    VERIFIED_TRUE = "true", _("Verified True")
    VERIFIED_FALSE = "false", _("Verified False")
    SPAM = "spam", _("Verified Spam")
    CANNOT_BE_VERIFIED = "unidentified", _("Cannot be verified")
