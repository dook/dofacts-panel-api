from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class StorageServiceInternalException(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Storage service error.")
    default_code = "storage_service_error"
