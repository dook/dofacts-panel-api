from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from dook.admin.permissions import IsAdmin
from dook.admin.serializers import (
    ExpertListSerializer,
    FactCheckerListSerializer,
    InvitationListSerializer,
    NewsDetailSerializer,
    NewsListSerializer,
    NewsUpdateSerializer,
    SensitiveKeywordManagementSerializer,
    UserDetailSerializer,
)
from dook.news.api.filters import AdminNewsFilter
from dook.news.models import News, SensitiveKeyword
from dook.users.filters import AdminUsersFilter
from dook.users.models import Invitation, User


class ExpertListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)

    model = User
    serializer_class = ExpertListSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering = ["-name"]
    search_fields = ["name", "email"]
    filterset_class = AdminUsersFilter

    def get_queryset(self):
        return self.model.objects.experts_with_opinions_count().with_assigned_news_count()


class FactCheckerListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)

    model = User
    serializer_class = FactCheckerListSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering = ["-name"]
    search_fields = ["name", "email"]
    filterset_class = AdminUsersFilter

    def get_queryset(self):
        return (
            self.model.objects.fact_checkers_with_opinions_count().with_assigned_news_count()
        )


class InvitationListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = Invitation.objects.all()
    serializer_class = InvitationListSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = UserDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(pk=self.kwargs["pk"])


class NewsListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = NewsListSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["reported_at"]
    ordering = ["-reported_at"]
    search_fields = ["text"]
    filterset_class = AdminNewsFilter

    model = News

    def get_queryset(self):
        return (
            self.model.objects.prefetch_related("expertopinion")
            .with_news_verdict_status()
            .with_is_duplicate()
        )


class NewsDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    http_method_names = ["get", "patch"]
    permission_classes = (IsAdmin,)
    serializer_class = NewsDetailSerializer
    serializer_action__class = {"PATCH": NewsUpdateSerializer}

    def get_serializer_class(self):
        return self.serializer_action__class.get(
            self.request.method, self.serializer_class
        )

    def get_queryset(self, *args, **kwargs):
        return (
            News.objects.filter(pk=self.kwargs["pk"])
            .with_fact_checker_opinions()
            .with_expert_opinions()
        )


class SensitiveKeywordListView(generics.ListCreateAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = SensitiveKeywordManagementSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ["-name"]
    search_fields = ["name"]
    queryset = SensitiveKeyword.objects.all()


class SensitiveKeywordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = SensitiveKeywordManagementSerializer
    queryset = SensitiveKeyword.objects.all()
