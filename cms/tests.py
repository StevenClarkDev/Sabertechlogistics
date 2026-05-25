from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import NavigationLink, Page, SiteSetting


class PublicPageTests(TestCase):
    def setUp(self):
        SiteSetting.objects.create(
            site_name='Saber Tech Logistics',
            site_url='https://sabertechlogistics.com',
            default_seo_description='Default logistics description.',
        )
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

    def test_page_seo_metadata_renders(self):
        self.about.seo_title = 'About SEO Title'
        self.about.seo_description = 'About SEO description.'
        self.about.seo_keywords = 'logistics, courier'
        self.about.seo_noindex = True
        self.about.save()
        response = self.client.get('/about/')
        self.assertContains(response, '<title>About SEO Title</title>', html=True)
        self.assertContains(response, 'name="description" content="About SEO description."')
        self.assertContains(response, 'name="keywords" content="logistics, courier"')
        self.assertContains(response, 'name="robots" content="noindex, follow"')
        self.assertContains(response, 'rel="canonical" href="https://sabertechlogistics.com/about/"')
        self.assertContains(response, 'property="og:title" content="About SEO Title"')
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"')

    def test_unpublished_page_returns_404(self):
        Page.objects.create(title='Hidden', slug='hidden', is_published=False)
        response = self.client.get('/hidden/')
        self.assertEqual(response.status_code, 404)


class SecurityThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        SiteSetting.objects.create(site_name='Saber Tech Logistics')
        Page.objects.create(title='Home', slug='', template='home', is_published=True)

    @override_settings(
        SECURITY_THROTTLE_ENABLED=True,
        SECURITY_THROTTLE_GENERAL_LIMIT=2,
        SECURITY_THROTTLE_GENERAL_WINDOW=60,
        SECURITY_THROTTLE_POST_LIMIT=20,
        SECURITY_THROTTLE_ADMIN_LIMIT=30,
    )
    def test_general_request_throttle_returns_429(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/').status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 429)
        self.assertEqual(response.headers['Retry-After'], '60')

    @override_settings(
        SECURITY_THROTTLE_ENABLED=True,
        SECURITY_THROTTLE_GENERAL_LIMIT=100,
        SECURITY_THROTTLE_POST_LIMIT=1,
        SECURITY_THROTTLE_POST_WINDOW=60,
        SECURITY_THROTTLE_ADMIN_LIMIT=30,
    )
    def test_write_request_throttle_returns_429(self):
        response = self.client.post('/contact-us/', {'name': 'A', 'email': 'a@example.com', 'message': 'Hello'})
        self.assertIn(response.status_code, {302, 404})
        response = self.client.post('/contact-us/', {'name': 'A', 'email': 'a@example.com', 'message': 'Hello'})
        self.assertEqual(response.status_code, 429)

    @override_settings(SECURITY_BLOCKED_PATH_PREFIXES=('/wp-login.php', '/.env'))
    def test_common_bot_probe_is_blocked_before_view_work(self):
        self.assertEqual(self.client.get('/wp-login.php').status_code, 404)
        self.assertEqual(self.client.get('/.env').status_code, 404)

# Create your tests here.
