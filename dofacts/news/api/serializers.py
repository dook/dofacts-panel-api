from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from dofacts.news.constants import VerdictType
from dofacts.news.models import ExpertOpinion, FactCheckerOpinion, News, NewsSensitiveKeyword


class ExpertOpinionSerializer(serializers.ModelSerializer):
    """
    ExpertOpinionSerializer is actually base class for serializing and validating
    opinions both for expert opinion case and as inheritance for fact checker.
    """

    title = serializers.CharField(required=False)
    about_corona_virus = serializers.BooleanField(required=False)
    confirmation_sources = serializers.CharField(required=False)
    verdict = serializers.ChoiceField(choices=VerdictType.choices, required=False)
    comment = serializers.CharField(required=False)
    is_duplicate = serializers.BooleanField(required=False)
    duplicate_reference = serializers.UUIDField(required=False)

    class Meta:
        model = ExpertOpinion
        fields = (
            "title",
            "about_corona_virus",
            "confirmation_sources",
            "verdict",
            "comment",
            "is_duplicate",
            "duplicate_reference",
        )

    def validate(self, data):
        """
        Validation is split into two main options:
        "verdict": "spam" <- incoming POST request should contain just this parameter.
        "is_duplicate": Boolean <- depending on "is_duplicate" value required_fields provides
            set of parameters that proper request should include.
        """

        required_fields = {
            True: {"is_duplicate", "duplicate_reference"},
            False: {
                "title",
                "about_corona_virus",
                "confirmation_sources",
                "verdict",
                "comment",
                "is_duplicate",
            },
        }

        verdict = data.get("verdict", "unidentified")
        if verdict == "spam":
            if len(data.keys()) != 1:
                raise ValidationError("Spam verdicts can not contain additional parameters")
            return data

        is_duplicate = data.get("is_duplicate", False)
        difference = required_fields[is_duplicate].difference(set(data.keys()))
        if difference:
            raise ValidationError(
                f"This request additionally requires { {*difference} } parameters"
            )
        return data


class FactCheckerOpinionSerializer(ExpertOpinionSerializer):
    class Meta(ExpertOpinionSerializer.Meta):
        model = FactCheckerOpinion
        fields = ExpertOpinionSerializer.Meta.fields


class SensitiveKeywordSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="sensitive_keyword.name")

    class Meta:
        model = NewsSensitiveKeyword
        fields = ("name",)


class NewsSerializerBase(serializers.ModelSerializer):
    """ Base Serializer Class for listing News instances """

    class Meta:
        fields = (
            "id",
            "url",
            "screenshot_url",
            "text",
            "reported_at",
            "comment",
        )


class ExpertNewsSerializer(NewsSerializerBase):
    expertopinion = ExpertOpinionSerializer(many=False, read_only=True)
    factcheckeropinion_set = FactCheckerOpinionSerializer(many=True, read_only=True)
    newssensitivekeyword_set = SensitiveKeywordSerializer(many=True, read_only=True,)

    current_verdict = serializers.SerializerMethodField()
    is_duplicate = serializers.SerializerMethodField()
    is_about_corona_virus = serializers.SerializerMethodField()
    is_spam = serializers.SerializerMethodField()

    class Meta(NewsSerializerBase):
        model = News
        read_only = True
        fields = NewsSerializerBase.Meta.fields + (
            "current_verdict",
            "is_duplicate",
            "is_about_corona_virus",
            "expertopinion",
            "factcheckeropinion_set",
            "is_spam",
            "newssensitivekeyword_set",
            "is_sensitive",
        )

    def get_current_verdict(self, obj):
        return obj.current_verdict

    def get_is_duplicate(self, obj):
        return obj.is_duplicate

    def get_is_about_corona_virus(self, obj):
        return True if obj.is_about_corona_virus else False

    def get_is_spam(self, obj):
        return obj.is_spam


class FactCheckerNewsSerializer(NewsSerializerBase):
    assigned_at = serializers.SerializerMethodField()
    is_opined = serializers.SerializerMethodField()

    class Meta(NewsSerializerBase.Meta):
        model = News
        read_only = True
        fields = NewsSerializerBase.Meta.fields + ("assigned_at", "is_opined",)

    def get_assigned_at(self, obj):
        return obj.assigned_at

    def get_is_opined(self, obj):
        return True if obj.is_opined else False


class NewsVerifiedSerializer(NewsSerializerBase):
    expertopinion = ExpertOpinionSerializer(many=False, read_only=True,)
    factcheckeropinion_set = FactCheckerOpinionSerializer(many=True, read_only=True)

    current_verdict = serializers.SerializerMethodField()
    is_duplicate = serializers.SerializerMethodField()
    is_about_corona_virus = serializers.SerializerMethodField()
    is_assigned_to_me = serializers.SerializerMethodField()

    class Meta(NewsSerializerBase.Meta):
        model = News
        fields = NewsSerializerBase.Meta.fields + (
            "expertopinion",
            "factcheckeropinion_set",
            "current_verdict",
            "is_duplicate",
            "is_about_corona_virus",
            "is_assigned_to_me",
        )

    def get_current_verdict(self, obj):
        return obj.current_verdict

    def get_is_duplicate(self, obj):
        return obj.is_duplicate

    def get_is_about_corona_virus(self, obj):
        return True if obj.is_about_corona_virus else False

    def get_is_assigned_to_me(self, obj):
        return obj.is_assigned_to_me
