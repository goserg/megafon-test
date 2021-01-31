from django.test import TestCase
from main.forms import ParseForm


class TestParseForm(TestCase):

  def test_parse_form_valid(self):
    form = ParseForm(data={
      'value': 10.0,
      'hasNds': True,
      'nds': 10.0,
      'parsed': 'some parsed text'
    })

    self.assertTrue(form.is_valid())

  def test_parse_form_no_data(self):
    form = ParseForm(data={})

    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)
  
  def test_parse_form_wrong_data(self):
    form = ParseForm(data={
      'value': True,
      'nds': True
    })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 2)
