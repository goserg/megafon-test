from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from main.models import Money

import time


class TestHomePage(StaticLiveServerTestCase):
  
  def setUp(self):
    self.browser = webdriver.Chrome('main/functional_tests/chromedriver.exe')

  def test_empty_history(self):
    self.browser.get(self.live_server_url)


  def test_history_is_displyed(self):
    money1 = Money.objects.create(
      value=10.0,
      hasNds=True,
      nds=10.0,
      parsed='some parsed text'
    )

    self.browser.get(self.live_server_url)
    self.assertEquals(
      self.browser.find_element_by_class_name('history__item').text,
      money1.parsed
    )

  def test_submitting_form(self):
    self.browser.get(self.live_server_url)

    value_input = self.browser.find_element_by_id('id_value')
    nds_checkbox = self.browser.find_element_by_id('check_1')
    nds_input = self.browser.find_element_by_id('id_nds')
    submit_button = self.browser.find_element_by_class_name('input-form__button')

    value_input.send_keys('6310.3')
    nds_checkbox.click()
    nds_input.send_keys('10')
    submit_button.click()

    self.assertEquals(
      self.browser.find_element_by_class_name('history__item').text,
      "6 941,33 (шесть тысяч девятьсот сорок один) рубль 33 копейки, включая НДС (10%) в сумме 631,03 (шестьсот тридцать один) рубль 03 копейки."
    )

    value_input = self.browser.find_element_by_id('id_value')
    nds_checkbox = self.browser.find_element_by_id('check_1')
    nds_input = self.browser.find_element_by_id('id_nds')
    submit_button = self.browser.find_element_by_class_name('input-form__button')

    value_input.send_keys('100')
    nds_checkbox.click()
    nds_input.send_keys('0')
    submit_button.click()

    self.assertEquals(
      self.browser.find_elements_by_class_name('history__item')[-1].text,
      "100 (сто) рублей."
    )


  def tearDown(self):
    self.browser.close()