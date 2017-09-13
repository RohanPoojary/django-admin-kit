import json
from django.http import HttpResponse

class Ajax:
    @classmethod
    def route(cls, key, module_cls, params):
        output = module_cls.run(key)
        json_output = json.dumps(output)
        response = HttpResponse(json_output)
        response['Content-Type'] = 'application/json'
        return response
