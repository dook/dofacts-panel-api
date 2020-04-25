from django.urls import include, re_path
from rest_framework import routers

from dook.news.api.views import (
    ExpertNewsViewSet,
    FactCheckerNewsViewSet,
    NewsVerifiedViewSet,
)

router = routers.DefaultRouter()

router.register(r"fact_checker/news", FactCheckerNewsViewSet, basename="fc-news")
router.register(r"expert/news", ExpertNewsViewSet, basename="expert-news")

router.register(r"news_verified", NewsVerifiedViewSet, basename="news-verified")

url_patterns = [re_path("", include(router.urls))]
