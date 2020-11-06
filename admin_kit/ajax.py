"""
    Admin Kit Ajax module

"""

import json
import re

from django.http import HttpResponse
from django.template.defaultfilters import slugify

class Ajax:
    """
    This is the base class for Ajax functionality.

    response_type : str
        The response type of the API. By default its set to ``json``, It also accepts ``text``.
    unique : bool
        If True, the ``key`` is prepended with class name slug, Thus making it unique per
        class.

    """
    response_type = 'json'
    unique = False

    def run(self, request, **kwargs):
        """
        This method should be overrided by the child class.

        """
        return "Hello World"

    def route(self, request, **kwargs):
        """
        For a given request it executes the ``run`` method of the ``module_cls`` and returns
        the response

        """
        output = self.run(request, **kwargs)
        return self.format_response(output)

    @classmethod
    def generate_key(cls, key):
        """
        A class method that generates key, that maps to the function

        If ``unique`` attribute is true, then it appends hiphen seperated class name to actual
        ``key``

        **Example**::

            >>> import DummyAjaxClass
            >>> DummyAjaxClass.generateKey('the_key')
            the_key
            >>> DummyAjaxClass.unique = True
            >>> DummyAjaxClass.generateKey('the_key')
            dummy-ajax-class-the_key

        """
        if cls.unique:
            word_splits = re.findall(r'([A-Za-z][a-z]+|[A-Z]+)', cls.__name__)
            key = slugify(' '.join(word_splits)) + '-' + key
        return key

    def format_response(self, output):
        """
        Formats the response type based on ``response_type`` attribute.

        """
        if self.response_type == 'json':
            json_output = json.dumps(output)
            response = HttpResponse(json_output)
            response['Content-Type'] = 'application/json'
        else:
            if output != None:
                response = HttpResponse(str(output))
            else:
                response = HttpResponse(json.dumps(
                    {
                        "no_return": True 
                    }
                ))
                response['Content-Type'] = 'application/json'
        return response
