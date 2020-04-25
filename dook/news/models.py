import uuid
from collections import Counter

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

from dook.events.mixins import ModelEventMixin
from dook.news.constants import VerdictType
from dook.news.events import NewsEvents
from dook.news.managers import NewsManager, NewsSensitiveKeywordsManager
from dook.users.constants import UserRoleType
from dook.users.models import User


class News(ModelEventMixin, models.Model):
    """
    News model representing object gathered from screenshot app.
    screenshot_url: identifies image resource on AWS S3.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    url = models.URLField(max_length=2000)
    screenshot_url = models.CharField(max_length=1000, blank=True)
    reporter_email = models.EmailField(blank=False)
    reported_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    text = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    is_sensitive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    deleted = models.BooleanField(default=False)

    sensitive_keywords = models.ManyToManyField(
        "news.SensitiveKeyword", through="NewsSensitiveKeyword"
    )

    objects = NewsManager()
    events_class = NewsEvents

    def is_with_verdict(self):
        self._verdict = None
        expected_verditcs = [
            VerdictType.VERIFIED_TRUE.value,
            VerdictType.VERIFIED_FALSE.value,
        ]

        try:
            self._verdict = (
                self.expertopinion.verdict
                if self.expertopinion.verdict in expected_verditcs
                else None
            )
        except ObjectDoesNotExist:
            pass

        if not self._verdict:
            counted_opinions_verdicts = Counter(
                self.factcheckeropinion_set.values_list("verdict", flat=True)
            )
            for v in expected_verditcs:
                if counted_opinions_verdicts[v] >= 2:
                    self._verdict = v

        return True if self._verdict else False

    def leave_opinion(self, user, opinion_params):
        whose_opinion = {
            UserRoleType.FACT_CHECKER: FactCheckerOpinion,
            UserRoleType.EXPERT: ExpertOpinion,
        }

        opinion_model = whose_opinion[user.role]

        try:
            opinion, created = opinion_model.objects.get_or_create(
                news=self, judge=user, defaults=opinion_params
            )
            if created:
                opinion.save()

                return opinion

        except IntegrityError:

            return None


class OpinionBase(models.Model):
    """
    OpinionBase model is a system base representation of opinion for an corresponding News instance.
    """

    judge = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        related_query_name="%(class)s",
    )
    verdict = models.CharField(
        max_length=50,
        choices=VerdictType.choices,
        default=VerdictType.CANNOT_BE_VERIFIED,
    )

    title = models.TextField(blank=False)
    comment = models.TextField(blank=True)
    confirmation_sources = models.TextField(blank=True)
    about_corona_virus = models.BooleanField(default=True)
    is_duplicate = models.BooleanField(default=False)
    duplicate_reference = models.UUIDField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True
        unique_together = ["news", "judge"]


class FactCheckerOpinion(OpinionBase):
    """
    FastCheckerOpinion model is case specific for opinion judged by user with FastChecker role in the system.
    """

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
        related_query_name="%(class)s",
    )

    class Meta(OpinionBase.Meta):
        db_table = "fact_checker_opinion"


class ExpertOpinion(OpinionBase):
    """
    ExpertOpinion model is case specific for opinion judged by user with Expert role in the system.
    """

    news = models.OneToOneField(News, on_delete=models.CASCADE, primary_key=False,)

    class Meta(OpinionBase.Meta):
        db_table = "expert_opinion"


class Keyword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    name = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._meta.model.__name__}, name: {self.name}"


class SensitiveKeyword(Keyword):
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class NewsSensitiveKeyword(models.Model):
    sensitive_keyword = models.ForeignKey(
        SensitiveKeyword,
        on_delete=models.CASCADE,
        related_name="newssensitivekeyword_set",
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    objects = NewsSensitiveKeywordsManager()
