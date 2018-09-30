import json
from urllib.parse import urlparse
from django.http import QueryDict


class AllowLocalhost:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.META.get('HTTP_REFERER') is None:
            return response
        url = urlparse(request.META.get('HTTP_REFERER'))
        refer = url.netloc
        scheme = url.scheme
        if refer.startswith('localhost'):
            response['Access-Control-Allow-Origin'] = scheme + '://' + refer
            response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


class JSONMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('CONTENT_TYPE') and 'application/json' in request.META['CONTENT_TYPE']:
            data = json.loads(request.body)
            q_data = QueryDict('', mutable=True)
            for key, value in data.items():
                if isinstance(value, list):
                    for x in value:
                        q_data.update({key: x})
                else:
                    q_data.update({key: value})

            if request.method == 'GET':
                request.GET = q_data

            if request.method == 'POST':
                request.POST = q_data

        return self.get_response(request)
