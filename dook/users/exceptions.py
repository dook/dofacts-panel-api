from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class InternalEmailErrorException(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Wystąpił błąd wewnętrzny poczty, nie udało się wysłać maila")
    default_code = "email_error"


class UserAlreadyExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Użytkownik z podanym mailem już istnieje.")
    default_code = "provided_email_error"


class InvalidInviteTokenException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Nieprawidłowy link.")
    default_code = "invalid_token_error"


class TokenAlreadyUsedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Link do rejestracji został już wykorzystany.")
    default_code = "invalid_token_error"


class InternalSignUpErrorException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Wystąpił błąd. Rejestracja nie powiodła się.")
    default_code = "sign_up_error"


class TokenAlreadyExpiredException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Link aktywacyjny wygasł.")
    default_code = "token_expired"


class EmailAlreadyConfirmedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Konto zostało już potwierdzone.")
    default_code = "already_confirmed"


class InvalidActivationUrlException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Nieprawidłowy link aktywacyjny")
    default_code = "invalid_activation_url"


class InactiveAccountException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Konto użytkownika nie jest aktywne.")
    default_code = "inactive_account"


class PasswordConfirmationFailedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Podane hasła muszą się zgadzać.")
    default_code = "password_confirmation_failed"


class EmailNotVerifiedException(exceptions.APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _(
        "Email użytkownika nie został potwierdzony. Potwierdź adres email."
    )
    default_code = "email_not_verified"


class InvalidCredentialsException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Podane nieprawidłowy email lub hasło, sprawdź podane dane.")
    default_code = "invalid_credentials"


class UserDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("Użytkownik nie istnieje.")
    default_code = "user_does_not_exist"


class PasswordTooWeakException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Podane hasło nie spełnia zasad bezpieczeństwa.")
    default_code = "password_too_weak"


class InvalidPasswordException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Podane hasło jest nieprawidłowe")
    default_code = "invalid_password"


class InvitationAlreadyExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Zaproszenie na podany email zostało już wysłane.")
    default_code = "invitation_already_exist"
