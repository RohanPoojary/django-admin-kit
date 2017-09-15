from django.test import TestCase
from django.shortcuts import reverse
from . import ajax

class AjaxUrlTestCase(TestCase):

    def test_ajax_response(self):
        ajax_url = reverse('admin_kit:ajax', args=('test-genres',))
        response = self.client.get(ajax_url)
        self.assertEqual(response.status_code, 200)
        
        json_response = response.json()
        actual_response = [
            ['thriller', 'thriller'],
            ['philosophy', 'philosophy']
        ]
        self.assertEqual(json_response, actual_response)