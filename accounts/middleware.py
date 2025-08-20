from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# from django.core.exceptions import ImproperlyConfigured
import logging

logger = logging.getLogger(__name__)

class CustomCSRFMiddleware(CsrfViewMiddleware):
    def process_response(self, request, response):
        response = super().process_response(request, response)
        if request.path == reverse('logout'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     if request.path == reverse('logout'):
    #         return None
    #     return super().process_view(request, callback, callback_args, callback_kwargs)