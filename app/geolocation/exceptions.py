from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def base_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

        if response is not None:
            response.data['status_code'] = response.status_code

    return response

class ExternalApiException(APIException):

    detail = None

    def __init__(self, message):
        ExternalApiException.detail = message