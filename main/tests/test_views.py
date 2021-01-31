from django.test import TestCase, Client
from django.urls import reverse
from main.models import Money


class TestViews(TestCase):

  def setUp(self):
    self.client = Client()
    self.home_url = reverse('home')

  def test_money_GET(self):
    response = self.client.get(self.home_url)

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'index.html')

  def test_money_POST_adds_new_money_item(self):
    response = self.client.post(self.home_url, {
      'value': 10.0,
      'hasNds': True,
      'nds': 20.0,
    })
    self.assertEquals(response.status_code, 200)
    self.assertEquals(Money.objects.first().parsed, "12,00 (двенадцать) рублей, включая НДС (20.0%) в сумме 2,00 (два) рубля.")