import factory
from django.utils import timezone

from dofacts.news.models import (
    ExpertOpinion,
    FactCheckerOpinion,
    News,
    NewsSensitiveKeyword,
    OpinionBase,
    SensitiveKeyword,
)
from dofacts.users.constants import UserRoleType
from tests.factories.users import UserFactory


class NewsFactory(factory.DjangoModelFactory):
    class Meta:
        model = News

    url = factory.Faker("uri")
    screenshot_url = factory.Faker("uri")
    reporter_email = factory.Faker("email")
    reported_at = factory.LazyFunction(timezone.now)
    text = factory.Faker("text")
    comment = factory.Faker("sentence")


class OpinionBaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = OpinionBase
        abstract = True

    news = factory.SubFactory(NewsFactory)
    title = factory.Faker("sentence")
    comment = factory.Faker("text")
    confirmation_sources = factory.Faker("uri")


class FactCheckerOpinionFactory(OpinionBaseFactory):
    class Meta:
        model = FactCheckerOpinion

    judge = factory.SubFactory(UserFactory, role=UserRoleType.FACT_CHECKER)


class ExpertOpinionFactory(OpinionBaseFactory):
    class Meta:
        model = ExpertOpinion

    judge = factory.SubFactory(UserFactory, role=UserRoleType.EXPERT)


class KeywordFactory(factory.DjangoModelFactory):
    class Meta:
        model = SensitiveKeyword

    name = factory.Faker("sentence")


class NewsKeywordFactory(factory.DjangoModelFactory):
    class Meta:
        model = NewsSensitiveKeyword

    keyword = factory.SubFactory("tests.factories.news.KeywordFactory")
    news = factory.SubFactory("tests.factories.news.NewsFactory")
