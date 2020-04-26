from django_filters.rest_framework import FilterSet, filters

from dofacts.users.constants import UserSpecializationType
from dofacts.users.models import User


class AdminUsersFilter(FilterSet):
    specialization = filters.ChoiceFilter(
        field_name="specialization", choices=UserSpecializationType.choices
    )
    created = filters.DateFromToRangeFilter(field_name="created_at")
    verified = filters.NumericRangeFilter(field_name="verified")

    class Meta:
        model = User
        fields = ("specialization", "created", "verified")
