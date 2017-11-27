from django.test import TestCase
from django.contrib.auth.models import User
from django.test.selenium import SeleniumTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from django.contrib.staticfiles.handlers import StaticFilesHandler

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .models import Author, Book

class TestModule(SeleniumTestCase):

    static_handler = StaticFilesHandler
    browser = 'chrome'

    @classmethod
    def setUpClass(cls):
        author = Author(name='author')
        author.save()
        book = Book(name='book', genres=['thriller', 'philosophy'])
        book.author = author
        book.save()

        User.objects.create_superuser(username='super', password='secret',
                                                  email='super@example.com')
        super(TestModule, cls).setUpClass()

    def login(self):
        timeout = 2
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.client.login(username='super', password='secret')
        cookie = self.client.cookies['sessionid']
        self.selenium.get(self.live_server_url + reverse('admin:login'))
        self.selenium.add_cookie(
            {'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'}
        )
        self.selenium.refresh()

    def test_if_duplicate_button_exists(self):
        self.login()
        self.selenium.get(self.live_server_url + '/admin/test_duplicate/author/1')
        WebDriverWait(self.selenium, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Add a Duplicate'))
        )
