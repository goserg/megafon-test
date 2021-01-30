from django.test import TestCase, Client
from django.urls import reverse
from main.models import Money


class TestViews(TestCase):

  def test_money_GET(self):
    client = Client()
    response = client.get(reverse('home'))

    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'index.html')