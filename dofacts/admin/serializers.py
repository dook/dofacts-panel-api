from rest_framework import serializers

from dofacts.news.api.serializers import SensitiveKeywordSerializer
from dofacts.news.models import ExpertOpinion, FactCheckerOpinion, News, SensitiveKeyword
from dofacts.users.models import Invitation, User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role", "is_active"]


class BaseUserListSerializer(serializers.ModelSerializer):
    assigned = serializers.SerializerMethodField()
    verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "specialization",
            "created_at",
            "is_active",
            "assigned",
            "verified",
        ]

    def get_assigned(self, obj):
        return obj.assigned

    def get_verified(self, obj):
        return obj.verified


class ExpertListSerializer(BaseUserListSerializer):
    pass


class FactCheckerListSerializer(BaseUserListSerializer):
    pass


class InvitationListSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ["id", "email", "sent_at", "status", "expired"]

    def get_expired(self, obj):
        return obj.key_expired()


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class FactCheckerOpinionExtendedSerializer(serializers.ModelSerializer):
    judge = JudgeSerializer(many=False, read_only=True)

    class Meta:
        model = FactCheckerOpinion
        fields = (
            "title",
            "about_corona_virus",
            "confirmation_sources",
            "verdict",
            "comment",
            "is_duplicate",
            "duplicate_reference",
            "judge",
        )


class ExpertOpinionExtendedSerializer(serializers.ModelSerializer):
    judge = JudgeSerializer(many=False, read_only=True)

    class Meta:
        model = ExpertOpinion
        fields = FactCheckerOpinionExtendedSerializer.Meta.fields


class NewsListSerializer(serializers.ModelSerializer):
    current_verdict = serializers.SerializerMethodField()
    is_duplicate = serializers.SerializerMethodField()
    newssensitivekeyword_set = SensitiveKeywordSerializer(many=True, read_only=True,)

    class Meta:
        model = News
        read_only = True
        fields = (
            "id",
            "url",
            "screenshot_url",
            "text",
            "reported_at",
            "comment",
            "current_verdict",
            "is_duplicate",
            "deleted",
            "newssensitivekeyword_set",
            "is_sensitive",
        )

    def get_current_verdict(self, obj):
        return obj.current_verdict

    def get_is_duplicate(self, obj):
        return obj.is_duplicate


class NewsDetailSerializer(serializers.ModelSerializer):
    expertopinion = ExpertOpinionExtendedSerializer(many=False, read_only=True,)
    factcheckeropinion_set = FactCheckerOpinionExtendedSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = (
            "id",
            "url",
            "screenshot_url",
            "text",
            "reported_at",
            "expertopinion",
            "factcheckeropinion_set",
            "deleted",
        )


class NewsUpdateSerializer(serializers.ModelSerializer):
    deleted = serializers.BooleanField(required=True)

    class Meta:
        model = News
        fields = ("deleted",)


class SensitiveKeywordManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensitiveKeyword
        fields = "__all__"
