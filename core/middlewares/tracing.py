import uuid
from threading import local

_threadlocals = local()
__THREAD_KEY__ = 'b3_headers'
__DEFAULT_KEY__ = 'x-request-id'

__OPENCENSUS__HEADERS__ = (
    'traceparent',
    'grpc-trace-bin',
    'x-cloud-trace-context',
)
__GENERIC_HEADERS__ = (
    'x-request-id',
    'x-b3-traceid',
    'x-b3-spanid',
    'x-b3-parentspanid',
    'x-b3-sampled',
    'x-b3-flags',
    'x-ot-span-context'
)
__TRACE_HEADES__ = [*__OPENCENSUS__HEADERS__, *__GENERIC_HEADERS__]


class B3Tracing:
    def __init__(self, get_response):
        self.get_response = get_response

    def set_request_headers(self, request):
        r""" Set request tracing header to thread local.
        :param request:         `Request` object used for get action in `Django` view.
        :return:                `trace header` will store in threadlocal, None will return
        :rtype:                  None
        """
        b3_headers = dict()
        default_trace_header = {__DEFAULT_KEY__.upper(): str(uuid.uuid4())}
        request_keys = request.headers.keys()
        for key in request_keys:
            update_header = {} if key.lower() not in __TRACE_HEADES__ else {key: request.headers[key]}
            b3_headers.update(update_header)
        add_trace_header = default_trace_header if __DEFAULT_KEY__ not in b3_headers.keys() else {}
        request.META.update(add_trace_header)
        b3_headers.update(add_trace_header)
        setattr(_threadlocals, __THREAD_KEY__, b3_headers)

    def set_response_headers(self, response):
        r""" Retrive B3 tracing header to response headers.
        :param request: `Response` object to set headers.
        :rtype: None
        :return: `Response` object used for get metrics in `Django` view.
        """
        b3_headers = getattr(_threadlocals, __THREAD_KEY__, {})
        for header, content in b3_headers.items():
            response[header] = content
        return response

    def __call__(self, request):
        r""" Main Entry for log metrics middleware.
        :param request: `Request` object used for get metrics in `Django` view.
        :rtype: 'Reponse'
        :return: response the view return by view
        """
        self.set_request_headers(request)
        response = self.get_response(request)
        response = self.set_response_headers(response)
        return response
