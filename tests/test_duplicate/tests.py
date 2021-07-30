# from django.contrib.auth.models import User
# from django.test.selenium import SeleniumTestCase
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from django.contrib.staticfiles.handlers import StaticFilesHandler
#
# try:
#     from django.urls import reverse
# except ImportError:
#     from django.core.urlresolvers import reverse
#
# from .models import Author, Book
#
# class TestModule(SeleniumTestCase):
#
#     static_handler = StaticFilesHandler
#     fixtures = ['books.json']
#     browser = 'phantomjs'
# 
#     def setUp(self):
#         User.objects.create_superuser(username='super', password='secret',
#                                       email='super@example.com')
#         super(TestModule, self).setUp()
#
#     def login(self):
#         timeout = 2
#         WebDriverWait(self.selenium, timeout).until(
#             lambda driver: driver.find_element_by_tag_name('body'))
#         self.selenium.get(self.live_server_url + reverse('admin:login'))
#         # Fill login information of admin
#         username = self.selenium.find_element_by_id("id_username")
#         username.send_keys("super")
#         password = self.selenium.find_element_by_id("id_password")
#         password.send_keys("secret")
#         self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
#
#     def test_if_duplicate_button_exists(self):
#         self.login()
#         self.selenium.get(self.live_server_url + '/admin/test_duplicate/author/1')
#         WebDriverWait(self.selenium, 5).until(
#             EC.presence_of_element_located((By.LINK_TEXT, 'Add a Duplicate'))
#         )
#
#     def test_model_duplication(self):
#         self.login()
#         self.selenium.get(self.live_server_url + '/admin/test_duplicate/author/1')
#         self.selenium.find_element_by_xpath('//a[text()="Add a Duplicate"]').click()
#
#         name1 = self.selenium.find_element_by_id("id_book_set-0-name")
#         name2 = self.selenium.find_element_by_id("id_book_set-1-name")
#         self.assertEqual(name1.get_attribute('value'), name2.get_attribute('value'))
#
#         genres1 = self.selenium.find_element_by_id("id_book_set-0-genres")
#         genres2 = self.selenium.find_element_by_id("id_book_set-1-genres")
#         self.assertEqual(genres1.get_attribute('value'), genres2.get_attribute('value'))
#
#         genres1 = self.selenium.find_element_by_id("id_book_set-0-main_genre")
#         genres2 = self.selenium.find_element_by_id("id_book_set-1-main_genre")
#         self.assertEqual(genres1.get_attribute('value'), genres2.get_attribute('value'))
#
