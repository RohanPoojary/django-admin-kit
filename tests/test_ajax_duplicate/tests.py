# from django.contrib.auth.models import User
# from django.contrib.staticfiles.handlers import StaticFilesHandler
# from django.test.selenium import SeleniumTestCase
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support.ui import Select
#
# try:
#     from django.urls import reverse
# except ImportError:
#     from django.core.urlresolvers import reverse
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
#
#     def test_model_duplication(self):
#         self.login()
#         self.selenium.get(self.live_server_url + '/admin/test_ajax_duplicate/author/1')
#         self.initializeFields()
#         self.selenium.find_element_by_xpath('//a[text()="Add a Duplicate"]').click()
#
#         # WebDriverWait(self.selenium, 600).until(
#         #     EC.presence_of_element_located((By.LINK_TEXT, 'Add a aaaDuplicate'))
#         # )
#
#         name1 = self.selenium.find_element_by_id("id_book_set-0-name")
#         name2 = self.selenium.find_element_by_id("id_book_set-1-name")
#         assert name1.get_attribute('value') == name2.get_attribute('value')
#
#         genres1 = Select(self.selenium.find_element_by_id("id_book_set-0-genres"))
#         genres2 = Select(self.selenium.find_element_by_id("id_book_set-1-genres"))
#         # self.assertEqual(genres1.get_attribute('value'), '')
#         # self.assertEqual(genres2.get_attribute('value'), '')
#         self.assertEqual(
#         [ opt.get_attribute('value')    for opt in genres1.all_selected_options ],
#         [ opt.get_attribute('value')    for opt in genres2.all_selected_options ]
#         )
#         # assert genres1.get_attribute('value') == genres2.get_attribute('value')
#
#         # WebDriverWait(self.selenium, 600).until(
#         #     EC.presence_of_element_located((By.LINK_TEXT, 'Add a aaDuplicate'))
#         # )
#
#         f_genres1 = Select(self.selenium.find_element_by_id("id_book_set-0-filteredGenres"))
#         f_genres2 = Select(self.selenium.find_element_by_id("id_book_set-1-filteredGenres"))
#         self.assertEqual(
#         [ opt.get_attribute('value')    for opt in f_genres1.all_selected_options ],
#         [ opt.get_attribute('value')    for opt in f_genres2.all_selected_options ]
#         )
#         # self.assertEqual(f_genres1.get_attribute('value'), f_genres2.get_attribute('value'))
#
#         desc1 = self.selenium.find_element_by_id("id_book_set-0-description")
#         desc2 = self.selenium.find_element_by_id("id_book_set-1-description")
#         assert desc1.get_attribute('value') == desc2.get_attribute('value')
#
#
#     def initializeFields(self):
#         name = self.selenium.find_element_by_id("id_book_set-0-name")
#         name.clear()
#         name.send_keys('dummy')
#
#         self.selenium.implicitly_wait(1)
#
#         genres = Select(self.selenium.find_element_by_id("id_book_set-0-genres"))
#         genres.deselect_all()
#         genres.select_by_value('sci-fi')
#         genres.select_by_value('fictional')
#         genres.select_by_value('philosophy')
#
