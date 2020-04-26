from unittest import mock

import pytest
from assertpy import assert_that
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from dofacts.users.models import User
from dofacts.users.tokens import password_reset_token_generator
from tests.factories.users import UserFactory


class TestPasswordResetRequestView:
    @pytest.mark.django_db
    def test_success_request(self, api_client):
        with mock.patch.multiple(
            "dofacts.users.views", send_password_reset_email=mock.DEFAULT
        ) as mocked:
            mocked["send_password_reset_email"].return_value = True
            user = UserFactory(email="test@dook.pro")

            url = reverse(f"users:password_reset_request")
            response = api_client.post(url, {"email": user.email}, format="json")

            assert response.status_code == 200

            reset_url = password_reset_token_generator.make_url(user)

            assert mocked["send_password_reset_email"].called
            assert mocked["send_password_reset_email"].with_args(user.email, reset_url)

    @pytest.mark.django_db
    def test_request_invalid_email(self, api_client):
        with mock.patch.multiple(
            "dofacts.users.views", send_password_reset_email=mock.DEFAULT
        ) as mocked:
            url = reverse(f"users:password_reset_request")
            response = api_client.post(url, {"email": "some@email.com"}, format="json")

            assert response.status_code == 200
            assert mocked["send_password_reset_email"].called is False


class TestPasswordResetView:
    @pytest.fixture
    def default_reset_data(self):
        user = UserFactory(email="test@dofacts.pro")
        token = password_reset_token_generator.make_token(user=user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return {"user": user, "token": token, "uid": uid}

    @pytest.mark.django_db
    def test_success_reset_get(self, api_client, default_reset_data):
        url = reverse(
            f"users:password_reset",
            kwargs={"uidb64": default_reset_data["uid"], "token": default_reset_data["token"]},
        )
        response = api_client.get(url, format="json")

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_success_reset_post(self, api_client, default_reset_data):
        url = reverse(
            f"users:password_reset",
            kwargs={"uidb64": default_reset_data["uid"], "token": default_reset_data["token"]},
        )
        new_password = "Password54321!"
        data = {"password": new_password, "password2": new_password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == 200
        assert_that(default_reset_data["user"].check_password(raw_password=new_password))

    @pytest.mark.django_db
    def test_user_does_not_exist(self, api_client, default_reset_data):
        url = reverse(
            f"users:password_reset",
            kwargs={
                "uidb64": "MWU2NzUzMzMtMWJmMC00OTJjLWE2YzMtMGY4OTE5MmE1MGNl",
                "token": default_reset_data["token"],
            },
        )
        new_password = "Password54321!"
        data = {"password": new_password, "password2": new_password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert_that(response.data["detail"].code).is_equal_to("invalid_token_error")

    @pytest.mark.django_db
    def test_invalid_token(self, api_client, default_reset_data):
        url = reverse(
            f"users:password_reset",
            kwargs={"uidb64": default_reset_data["uid"], "token": "5ff-4409af0e1e600a7c78f9"},
        )
        new_password = "Password54321!"
        data = {"password": new_password, "password2": new_password}
        response = api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert_that(response.data["detail"].code).is_equal_to("invalid_token_error")
        assert_that(default_reset_data["user"].check_password(raw_password=new_password)).is_false()


class TestInternalPasswordResetView:
    @pytest.mark.django_db
    def test_success_reset(self, authenticated_api_client, default_user):
        url = reverse("users:internal_password_reset",)
        new_password = "Password54321!"
        data = {
            "old_password": "password",
            "password": new_password,
            "password2": new_password,
        }
        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == 200

        user = User.objects.filter(id=default_user.id).first()
        assert_that(user.check_password(new_password)).is_true()

    @pytest.mark.django_db
    def test_wrong_old_password(self, authenticated_api_client, default_user):
        url = reverse("users:internal_password_reset",)
        new_password = "Password54321!"
        data = {
            "old_password": "wrongpassword",
            "password": new_password,
            "password2": new_password,
        }
        response = authenticated_api_client.post(url, data, format="json")

        assert response.status_code == 400
        assert_that(default_user.check_password(new_password)).is_false()
