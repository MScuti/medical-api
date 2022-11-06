from requests import request
import requests as human_requests
from core.middlewares.tracing import _threadlocals

trace_headers = getattr(_threadlocals, 'trace_headers', {})


def get_trace_headers(kwargs):
    r"""Get trace header.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :dict:`extra header`
    :rtype: dict
    """
    add_headers = dict()
    for trace_header in trace_headers.items():
        add_headers.update(trace_header)
    if not add_headers:
        return add_headers
    if 'headers' not in kwargs.keys():
        return add_headers
    common_headers = (add_headers.keys() + kwargs['headers'].keys())
    for trace_header in common_headers:
        add_headers.pop(trace_header)
    return add_headers


def update_kwargs(kwargs):
    origin_headers = kwargs.get("headers", {})
    extra_headers = get_trace_headers(kwargs)
    if not extra_headers:
        return kwargs
    kwargs['headers'] = origin_headers.update(extra_headers)
    return kwargs


def get(url, params=None, **kwargs):
    r"""Sends a GET request.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    kwargs.setdefault('allow_redirects', True)
    return request('get', url, params=params, **kwargs)


def options(url, **kwargs):
    r"""Sends an OPTIONS request.
    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    kwargs.setdefault('allow_redirects', True)
    return request('options', url, **kwargs)


def head(url, **kwargs):
    r"""Sends a HEAD request.
    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes. If
        `allow_redirects` is not provided, it will be set to `False` (as
        opposed to the default :meth:`request` behavior).
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    r"""Sends a POST request.
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    return request('post', url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    r"""Sends a PUT request.
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    return request('put', url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    r"""Sends a PATCH request.
    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) json data to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    return request('patch', url, data=data, **kwargs)


def delete(url, **kwargs):
    r"""Sends a DELETE request.
    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    kwargs = update_kwargs(kwargs)
    return request('delete', url, **kwargs)


human_requests.get, human_requests.put, human_requests.head = get, put, head
human_requests.post, human_requests.patch, human_requests.delete, human_requests.options = post, patch, delete, options
requests = human_requests