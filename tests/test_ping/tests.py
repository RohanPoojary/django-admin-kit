from django.test.selenium import SeleniumTestCase
from django.contrib.staticfiles.handlers import StaticFilesHandler

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

class TestModule(SeleniumTestCase):

    static_handler = StaticFilesHandler
    browser = 'phantomjs'

    def test_if_ping_exists(self):
        self.selenium.get(self.live_server_url + '/admin_kit/ping')
        self.selenium.find_element_by_xpath('//h1[text()="PONG"]')
