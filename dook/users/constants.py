from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleType(models.TextChoices):
    BASE_USER = "base_user", _("Base User")
    FACT_CHECKER = "fact_checker", _("Fact Checker")
    EXPERT = "expert", _("Expert")
    ADMIN = "admin", _("Admin")


class UserSpecializationType(models.TextChoices):
    JOURNALISM = "journalism", _("Dziennikarstwo")
    BIOLOGY = "biology", _("Biologia")
    PHYSICS = "physics", _("Fizyka")
    IT = "IT", _("IT")
    CHEMISTRY = "chemistry", _("Chemia")
    ECONOMY = "economy", _("Ekonomia")
    OTHER = "other", _("Inna")


class InvitationStatusType(models.TextChoices):
    FAILED = "Błąd wysyłki", _("FAILED")
    WAITING = "Oczekujące", _("WAITING")
    IN_PROGRESS = "W trakcie", _("IN_PROGRESS")
    USED = "Wykorzystane", _("USED")


class InvitationUserRoleType(models.TextChoices):
    FACT_CHECKER = "fact_checker", _("Fact Checker")
    EXPERT = "expert", _("Expert")
