from django.test import TestCase
from django.urls import reverse, resolve
from main.views import home_view


class TestUrls(TestCase):

  def test_home_url_resolves(self):
    url = reverse('home')
    self.assertEquals(resolve(url).func, home_view)