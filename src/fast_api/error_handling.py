import logging
import os
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse


DEBUG = os.getenv('DEBUG', 0)

def report_exception(exc, level="warning"):
    # TODO add sentry settings
    try:
        import sentry_sdk
        with sentry_sdk.configure_scope() as scope:
            scope.level = level
            sentry_sdk.capture_exception(exc)

        sentry_sdk.capture_exception(exc)
    except:
        pass


def exception_handler(exc, context):
    from rest_framework.views import exception_handler

    response = exception_handler(exc, context)

    if response is not None:
        response.data["status_code"] = response.status_code
    elif isinstance(exc, AssertionError):
        err_data = {"error": str(exc)}
        logging.warning(exc)
        report_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)
    elif isinstance(exc, IntegrityError):
        err_data = {"error": str(exc)}
        logging.warning(exc)
        report_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, ObjectDoesNotExist):
        tb = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        err_data = {"error": "Doesn't exist"}
        logging.warning(exc)
        report_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, Exception):
        tb = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        err_data = {
            "error": "Unknown error"
        }
        if DEBUG:
            err_data['tb'] = tb
        logging.error(exc)
        logging.error(tb)
        report_exception(exc, "error")
        response = JsonResponse(err_data, safe=True, status=500)

    return response
