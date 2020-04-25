import factory
from django.utils import timezone

from dook.users.constants import UserRoleType
from dook.users.models import Invitation, User, UserNews


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")


class InvitationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Invitation

    sent_at = factory.LazyFunction(timezone.now)
    token = factory.LazyFunction(Invitation.next_token)
    email = factory.Faker("email")


class UserNewsFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserNews

    user = factory.SubFactory(UserFactory, role=UserRoleType.FACT_CHECKER)
    news = factory.SubFactory("tests.factories.news.NewsFactory")
