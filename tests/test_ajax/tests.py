import json
from django.test import TestCase

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

class AdminAjaxTest(TestCase):

    def test_if_ajax_registered(self):
        response = self.client.get(reverse("admin_kit:ajax", args=('testajax',)))
        data = json.loads(response.content)
        self.assertEqual(data, [
            ['book1', '1'],
            ['book2', '2']
        ])

    def test_unique_key(self):
        response = self.client.get(reverse("admin_kit:ajax", args=('test-empty-empty',)))
        self.assertEqual(response.content, b"Hello World")