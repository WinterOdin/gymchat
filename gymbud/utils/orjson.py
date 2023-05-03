try:
    import orjson as json
except ImportError:
    import json
from rest_framework.response import Response

class ORJsonResponse(Response):
    def __init__(self, data, safe=False, json_dumps_params=None, load=False, **kwargs):
        if safe and not isinstance(data, dict) and not load:
            raise TypeError(
                'In order to allow non-dict objects to be serialized set the '
                'safe parameter to False.'
            )
        if load and safe and not isinstance(data, (bytes, bytearray, str)):
            raise TypeError(
                'In order to allow non-bytes objects to be sent set the '
                'safe parameter to False.'
            )
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault('content_type', 'application/json')
        if not load:
            data = json.dumps(data, **json_dumps_params)
        super().__init__(data, **kwargs)

# class ORJsonResponse(HttpResponse):
#     def __init__(self, data, safe=False, json_dumps_params=None, load=False, **kwargs):
#         if safe and not isinstance(data, dict) and not load:
#             raise TypeError(
#                 'In order to allow non-dict objects to be serialized set the '
#                 'safe parameter to False.'
#             )
#         if load and safe and not isinstance(data, (bytes, bytearray, str)):
#             raise TypeError(
#                 'In order to allow non-bytes objects to be sent set the '
#                 'safe parameter to False.'
#             )
#         if json_dumps_params is None:
#             json_dumps_params = {}
#         kwargs.setdefault('content_type', 'application/json')
#         if not load:
#             data = json.dumps(data, **json_dumps_params)
#         super().__init__(content=data, **kwargs)
