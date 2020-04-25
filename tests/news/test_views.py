from unittest import mock

import pytest
from django.urls import reverse

from dook.news.constants import VerdictType
from dook.news.models import ExpertOpinion, FactCheckerOpinion
from dook.users.constants import (
    InvitationStatusType,
    InvitationUserRoleType,
    UserRoleType,
)
from tests.factories.news import (
    ExpertOpinionFactory,
    FactCheckerOpinionFactory,
    NewsFactory,
)
from tests.factories.users import UserFactory, UserNewsFactory


@pytest.fixture
def default_opinion_data():
    data = {
        "title": "Some random title",
        "about_corona_virus": True,
        "confirmation_sources": "drop.com",
        "verdict": VerdictType.VERIFIED_TRUE,
        "comment": "Thinking through all the facts and other dependencies, yes.",
        "is_duplicate": False,
    }
    return data


class TestExpertNewsViewSet:
    @pytest.mark.django_db
    def test_create_expert_opinion(self, api_client, default_opinion_data):
        with mock.patch.multiple(
            "dook.users.events", send_news_verified_notification=mock.DEFAULT
        ) as mocked:
            news = NewsFactory()
            user = UserFactory(role=UserRoleType.EXPERT)
            api_client.force_authenticate(user=user)

            url = reverse("api:expert-news-create_opinion", kwargs={"id": news.pk})
            response = api_client.post(url, default_opinion_data, format="json")

            expert_opinion = ExpertOpinion.objects.filter(news=news, judge=user).first()

            assert response.status_code == 201
            assert expert_opinion

            email_args = {
                "user_email": news.reporter_email,
                "news_pk": news.pk,
                "verdict_type": "VERIFIED_BY_EXPERT",
            }

            assert mocked["send_news_verified_notification"].called
            assert mocked["send_news_verified_notification"].call_args == mock.call(
                **email_args
            )

    @pytest.mark.django_db
    def test_already_verified_by_fcs(self, api_client, default_opinion_data):
        with mock.patch.multiple(
            "dook.users.events", send_news_verified_notification=mock.DEFAULT
        ) as mocked:
            news = NewsFactory()
            user = UserFactory(role=UserRoleType.EXPERT)

            FactCheckerOpinionFactory(news=news, verdict=VerdictType.VERIFIED_TRUE)
            FactCheckerOpinionFactory(news=news, verdict=VerdictType.VERIFIED_TRUE)

            api_client.force_authenticate(user=user)

            url = reverse("api:expert-news-create_opinion", kwargs={"id": news.pk})
            response = api_client.post(url, default_opinion_data, format="json")

            expert_opinion = ExpertOpinion.objects.filter(news=news, judge=user).first()

            assert response.status_code == 201
            assert expert_opinion

            email_args = {
                "user_email": news.reporter_email,
                "news_pk": news.pk,
                "verdict_type": "VERIFIED_BY_EXPERT",
            }

            assert mocked["send_news_verified_notification"].called
            assert mocked["send_news_verified_notification"].call_args == mock.call(
                **email_args
            )


class TestFactCheckerNewsViewSet:
    @pytest.mark.django_db
    def test_create_fc_opinion(self, api_client, default_opinion_data):
        with mock.patch.multiple(
            "dook.users.events", send_news_verified_notification=mock.DEFAULT
        ) as mocked:
            news = NewsFactory()
            user_1 = UserFactory(role=UserRoleType.FACT_CHECKER)
            user_2 = UserFactory(role=UserRoleType.FACT_CHECKER)

            UserNewsFactory(news=news, user=user_1)
            UserNewsFactory(news=news, user=user_2)

            url = reverse("api:fc-news-create_opinion", kwargs={"id": news.pk})

            api_client.force_authenticate(user=user_1)
            response = api_client.post(url, default_opinion_data, format="json")

            fc_opinion = FactCheckerOpinion.objects.filter(
                news=news, judge=user_1
            ).first()

            assert fc_opinion
            assert mocked["send_news_verified_notification"].called is False

            api_client.force_authenticate(user=user_2)
            response = api_client.post(url, default_opinion_data, format="json")

            fc_opinion = FactCheckerOpinion.objects.filter(
                news=news, judge=user_2
            ).first()

            assert fc_opinion
            assert response.status_code == 201

            email_args = {
                "user_email": news.reporter_email,
                "news_pk": news.pk,
                "verdict_type": "VERIFIED_BY_FACT_CHECKER",
            }

            assert mocked["send_news_verified_notification"].called
            assert mocked["send_news_verified_notification"].call_args == mock.call(
                **email_args
            )
