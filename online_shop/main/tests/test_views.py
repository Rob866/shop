from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/home.ht  ml')
        #self.assertContains(response,'data')
    def test_about_us_works(self):
        response = self.client.get(reverse('main:about_us'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'main/about_us.html')
