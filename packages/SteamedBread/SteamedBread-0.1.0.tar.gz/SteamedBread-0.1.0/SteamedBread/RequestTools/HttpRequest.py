"""
@Author: 馒头 (chocolate)
@Email: neihanshenshou@163.com
@File: HttpRequest.py
@Time: 2023/12/9 18:00
"""

import json as json_v2
from urllib import parse
from urllib.parse import unquote

from requests import Response
from requests import Session

from SteamedBread.LoggerTools.Logger import logger


def __hook_response(response: Response, **kwargs):
    try:
        result = json_v2.dumps(response.json(), ensure_ascii=False)
    except Exception as e:
        result = response.text or e

    kwargs = {"服务code码": response.status_code, **kwargs}
    query = unquote(parse.urlparse(response.url).query or parse.urlparse(response.url).params)

    logger.info(f"""
请求方法: {response.request.method}
请求地址: {response.request.url.split("?")[0]}
请求内容: {response.request.body or query or {} }
请求响应: {result}
请求时长: {response.elapsed.total_seconds()} 秒
更多内容: {kwargs}
    """)


def request(method, url, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.

    :param method: method for the new :
        class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response

    """

    with Session() as session:
        return session.request(method=method, url=url, hooks=dict(response=__hook_response), **kwargs)


def get(url, params=None, **kwargs):
    r"""Sends a GET request.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    r"""Sends an OPTIONS request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("options", url, **kwargs)


def head(url, **kwargs):
    r"""Sends a HEAD request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    r"""Sends a POST request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    r"""Sends a PUT request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    r"""Sends a PATCH request.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, list of tuples, bytes, or file-like
        object to send in the body of the :class:`Request`.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    r"""Sends a DELETE request.

    :param url: URL for the new :class:`Request` object.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """

    return request("delete", url, **kwargs)
