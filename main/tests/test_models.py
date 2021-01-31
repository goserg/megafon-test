from django.test import TestCase
from main.models import Money

class TestModels(TestCase):

  def setUp(self):
    self.money1 = Money.objects.create(
      value = 10.0,
      hasNds = True,
      nds = 10.0,
      parsed = 'test_parse'
    )
    pass