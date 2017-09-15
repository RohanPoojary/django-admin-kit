import json
import re

from django.http import HttpResponse, HttpRequest
from django.template.defaultfilters import slugify

class Ajax:
    response_type = 'json'
    query_name = 'q'
    unique = False

    @classmethod
    def route(cls, request, module_cls):
        output = module_cls.run(request)
        return module_cls.formatResponse(output)

    @classmethod
    def generateKey(cls, key, model_cls):
        if model_cls.unique:
            word_splits = re.findall(r'([A-Za-z][a-z]+|[A-Z]+)', model_cls.__name__)
            key = slugify(' '.join(word_splits)) + '-' + key
        return key

    def formatResponse(self, output):
        if self.response_type == 'json':
            json_output = json.dumps(output)
            response = HttpResponse(json_output)
            response['Content-Type'] = 'application/json'
        else:
            response = HttpResponse(str(output))
        return response
