"""
This module provides general http handler functions for 
processing http responses from AIHC services.
"""

import json
from baidubce.utils import Expando


def parse_json(http_response, response):
    body = http_response.read()
    if body:
        response.__dict__.update(json.loads(
            body, object_hook=dict_to_python_object).__dict__)
    http_response.close()
    return True


def dict_to_python_object(d):
    """

    :param d:
    :return:
    """
    attr = {}
    for k, v in list(d.items()):
        k = str(k)
        attr[k] = v
    return Expando(attr)
