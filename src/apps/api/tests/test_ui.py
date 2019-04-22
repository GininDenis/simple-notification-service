import time

from urllib.parse import urljoin

from django.test import LiveServerTestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from selenium import webdriver


class TestUITestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.base_url = self.live_server_url
        super().setUp()

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    def test_index_page(self):
        ui_url = urljoin(self.base_url, reverse('ui'))
        selenium = self.selenium
        selenium.get(ui_url)
        self.assertEqual(selenium.title, 'Simple Notification Service')
        page_header = selenium.find_element_by_id('main-header').text
        self.assertEqual(page_header, _('Personal Area'))
