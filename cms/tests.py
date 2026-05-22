from django.test import TestCase
from django.urls import reverse

from .models import NavigationLink, Page, SiteSetting


class PublicPageTests(TestCase):
    def setUp(self):
        SiteSetting.objects.create(site_name='Saber Tech Logistics')
        self.home = Page.objects.create(
            title='Home',
            slug='',
            template='home',
            is_published=True,
            show_in_main_nav=True,
        )
        self.about = Page.objects.create(
            title='About Saber Tech',
            slug='about',
            template='standard',
            is_published=True,
        )
        NavigationLink.objects.create(label='Home', url='/', location='header')

    def test_home_page_renders(self):
        response = self.client.get(reverse('cms:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home')

    def test_slug_page_renders(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Saber Tech')

    def test_unpublished_page_returns_404(self):
        Page.objects.create(title='Hidden', slug='hidden', is_published=False)
        response = self.client.get('/hidden/')
        self.assertEqual(response.status_code, 404)

# Create your tests here.
