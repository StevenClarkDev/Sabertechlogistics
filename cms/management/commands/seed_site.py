from django.core.management.base import BaseCommand

from cms.models import ContentBlock, NavigationLink, Page, SiteSetting, TeamMember


PAGES = [
    {
        'title': 'Every Delivery Executed with Absolute Reliability',
        'slug': '',
        'nav_label': 'Home',
        'template': 'home',
        'eyebrow': 'Secure. Transparent. Always.',
        'subtitle': 'Every order is managed with precision, transparency, and professionalism, giving you confidence and control over your delivery operations.',
        'body': '<p>Saber Tech empowers businesses with disciplined execution, seamless delivery, and operational precision. At Saber Tech, we redefine last-mile delivery by combining smart technology with disciplined, operator-led execution.</p>',
        'show_in_main_nav': True,
        'sort_order': 0,
    },
    {
        'title': 'ATMP Courier',
        'slug': 'atmp-courier',
        'template': 'standard',
        'subtitle': 'Welcome to Your Seamless Delivery Experience',
        'body': '<p>ATMP-Courier is a last-mile platform engineered to strengthen owner-operator profits through controlled delivery execution.</p><ul><li>Built Driver-First</li><li>Payment Secured Before Dispatch</li><li>Earnings Protected by Enforcement</li><li>Predictable, Professional Execution</li></ul>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 10,
    },
    {
        'title': 'ATMP-Core: Discipline Before Dispatch',
        'slug': 'atmp-core',
        'nav_label': 'ATMP-Core',
        'template': 'standard',
        'body': '<p>ATMP-core acts as a control gate for every delivery. Jobs only go live when drivers are available, vehicles are suitable, and terms are confirmed.</p><p>By enforcing readiness before movement, the system prevents breakdowns, delays, and wasted effort.</p>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 20,
    },
    {
        'title': 'Customer Order Portal',
        'slug': 'customer-order',
        'nav_label': 'Customer Order',
        'template': 'standard',
        'eyebrow': 'Customer',
        'subtitle': 'Use the ATMP-Courier Customer Portal to schedule deliveries effortlessly.',
        'body': '<p>The Customer Portal has smart scheduling, secure payments, and happy margins. It ensures every delivery is possible before it even hits the system.</p>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 30,
    },
    {
        'title': 'Driver Access Portal',
        'slug': 'driver-access',
        'nav_label': 'Driver Access',
        'template': 'standard',
        'eyebrow': 'Driver',
        'subtitle': 'Join or access the ATMP-Courier driver platform, built to make every dispatch smooth, fast, and hassle-free.',
        'body': '<p>Drivers connect with ATMP-Courier through our Progressive Web App, built for real-time dispatch. Smart notifications and enforced acceptance windows keep operations predictable.</p>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 40,
    },
    {
        'title': 'Executive Leadership',
        'slug': 'leadership',
        'nav_label': 'Leadership',
        'template': 'leadership',
        'subtitle': 'Saber Tech Executive Team',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 50,
    },
    {
        'title': 'Saber Tech Launches Cutting-Edge Platform to Transform Last-Mile Delivery',
        'slug': 'press',
        'nav_label': 'Press',
        'template': 'standard',
        'body': '<p>Saber Tech today announced the beta launch of its Last-Mile Courier Platform, a production-ready system the company operates to power real-world delivery execution and visibility.</p><p>The beta focuses exclusively on last-mile courier operations, delivering reliable dispatch coordination, real-time tracking, exception handling, and operational visibility across local and regional networks.</p><h2>Media Contact</h2><p>Val Olson<br>Chief Public Relations Officer<br>Saber Tech<br>Email: volson@sabertechlogistics.com</p>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 60,
    },
    {
        'title': 'Get in Touch with Saber Tech',
        'slug': 'contact-us',
        'nav_label': 'Contact Us',
        'template': 'contact',
        'eyebrow': 'Contact',
        'subtitle': 'Saber Tech is here to answer your questions, streamline your delivery needs, and provide reliable support whenever you need it.',
        'body': '<h2>Message</h2><p>Name, email, and message are required.</p>',
        'show_in_main_nav': True,
        'show_in_footer': True,
        'sort_order': 70,
    },
    {
        'title': 'About Saber Tech',
        'slug': 'about',
        'nav_label': 'About',
        'template': 'standard',
        'body': '<p>Saber Tech builds owner and operator centric logistics infrastructure for last-mile delivery execution.</p><p>Saber Tech is an infrastructure-first technology company focused on logistics execution systems designed for owners and operators.</p>',
        'show_in_footer': True,
        'sort_order': 80,
    },
    {
        'title': 'Privacy Policy',
        'slug': 'privacy-policy',
        'template': 'legal',
        'body': '<p>Effective Date: 1/29/26</p><p>Saber Tech operates the ATMP-Core and ATMP-Courier platforms, including all related websites, applications, and services. We are committed to protecting the privacy, confidentiality, and security of all users who interact with our Platform.</p><h2>1. Information We Collect</h2><p>We collect information necessary to operate a secure, efficient, and enforcement-driven logistics platform.</p><h2>2. How We Use Your Information</h2><p>We use collected information to operate and improve the Platform, including managing dispatch workflows, validating driver availability, enforcing acceptance windows, processing payments, preventing fraud, and maintaining system accountability.</p><h2>3. Data Sharing and Disclosure</h2><p>Saber Tech does not sell or rent personal data.</p>',
        'show_in_footer': True,
        'sort_order': 90,
    },
    {
        'title': 'Term & Condition',
        'slug': 'term-and-conditions',
        'template': 'legal',
        'body': '<p>Effective Date: 1/29/26</p><p>These Terms & Conditions govern your access to and use of the ATMP-Core and ATMP-Courier platforms operated by Saber Tech.</p><h2>1. Platform Purpose</h2><p>ATMP-Courier is an operational logistics and last-mile delivery platform designed to manage dispatch execution, driver availability enforcement, payment validation, and delivery accountability.</p><h2>2. User Eligibility</h2><p>You must be at least 18 years old to use the Platform.</p><h2>3. Account Registration & Responsibility</h2><p>Users are responsible for maintaining accurate account information and safeguarding login credentials.</p>',
        'show_in_footer': True,
        'sort_order': 100,
    },
]

BLOCKS = {
    '': [
        ('Get Started', 'Submit delivery details quickly through our platform for seamless scheduling.', 'Get Started', '/atmp-courier/'),
        ('Learn More', 'Explore the command layer that protects every delivery before dispatch.', 'Learn More', '/atmp-core/'),
        ('iOS - Driver', 'Download the SaberTech Driver app from the App Store.', 'iOS - Driver', 'https://apps.apple.com/gb/app/sabertech-driver/id6759118586'),
        ('Android - Driver', 'Download the SaberTech Driver app from Google Play.', 'Android - Driver', 'https://play.google.com/store/apps/details?id=com.sabertech.driver'),
        ('From Pickup to Perfect Delivery', 'Place your order, get a driver assigned, track in real time, and confirm successful delivery.', '', ''),
        ('Delivery With Complete Accountability', 'Our platform coordinates drivers, pickups, and drop-offs, simplifying delivery operations for businesses across multiple markets.', 'Launch Customer Order Portal', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/customer-pwa/'),
        ('Every Package, Perfectly Managed', 'Business delivery, consumer shipments, e-commerce support, multi-market coverage, real-time tracking, professional drivers, transparent operations, and platform-powered efficiency.', 'Read More About ATMP-Courier', '/atmp-courier/'),
        ('Driver Access', 'Sign up or log in to the ATMP-Courier driver platform for seamless, efficient dispatch management.', 'Driver Sign Up', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-signup/'),
    ],
    'atmp-courier': [
        ('Driver Sign Up', 'Drivers start by completing the ATMP-Courier sign-up, providing key personal and location info to ensure smooth verification.', 'Begin Driver Sign Up', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-signup/'),
        ('Verification & Documents', 'Drivers submit license, insurance, registration, vehicle details, and screening documents before accepting jobs.', '', ''),
        ('Dispatch Rules', 'Mandatory alerts, acceptance windows, reassignment, vehicle enforcement, and paid tracked jobs keep dispatch disciplined.', '', ''),
        ('Driver App Features', 'Runs in a browser, installs to the home screen, supports push notifications, and updates automatically.', '', ''),
        ('Earnings & Protections', 'Jobs paid before dispatch, reduced downtime, clear details upfront, and no platform cuts.', '', ''),
    ],
    'atmp-core': [
        ('Control Before Motion', 'Every delivery decision should be made before the wheels move.', '', ''),
        ('Design Goal', 'Protect revenue by enforcing rules before execution.', '', ''),
        ('Systems That Enforce Discipline', 'Expansion by design, funds first, verified readiness, and right-fit vehicle matching.', '', ''),
    ],
    'customer-order': [
        ('Live Access', 'This link opens in a new tab.', 'Launch Customer Order Portal', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/customer-pwa/'),
        ('Why ATMP Uses Progressive Web Apps', 'PWAs deliver real-time push notifications, offline resilience, secure access, and instant updates.', '', ''),
    ],
    'driver-access': [
        ('Driver Sign Up', 'Start your driver onboarding and verification.', 'Driver Sign Up', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-signup/'),
        ('Driver Sign In', 'Access the ATMP-Courier driver platform.', 'Driver Sign In', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-pwa/'),
        ('Why ATMP Uses Progressive Web Apps', 'PWAs keep operations consistent across devices without app store delays.', '', ''),
    ],
}

TEAM = [
    ('Megan Patrick', 'Chief Executive Officer', 'mpatrick@sabertechlogistics.com', '(907) 250-8765', 'team/ceo-1.jpg', True),
    ('Sharon Culpepper', 'Chief Personnel Officer', 'sculpepper@sabertechlogistics.com', '', 'team/cpo-1.jpg', False),
    ('Val Olson', 'Chief Public Relations Officer', 'volson@sabertechlogistics.com', '', 'team/cpro-1.jpg', False),
    ('Cory Rankin', 'Chief Operating Officer', 'crankin@sabertechlogistics.com', '', 'team/coo-1.jpg', True),
    ('Jennifer Rynearson', 'Chief Logistics Officer', 'jrynearson@sabertechlogistics.com', '', 'team/clo-1.jpg', False),
    ('Christine Alva Armas', 'Chief Vision Officer', 'carmas@sabertechlogistics.com', '', 'team/cvo-1.jpg', False),
    ('Hamza Bhatti', 'Chief Technology Officer', '', '', 'team/cto-1.jpg', True),
    ('Afnan Ahmed Bhutto', 'Chief Marketing Officer', '', '', 'team/cmo-1.jpg', False),
    ('Ian Carter', 'Chief Communications Officer', 'icarter@sabertechlogistics.com', '', 'team/cco-1.jpg', False),
    ('Anli Goldsmith', 'Chief Science Officer', 'cagoldsmith@sabertechlogistics.com', '', '', False),
]


class Command(BaseCommand):
    help = 'Seed editable CMS content from the initial WordPress migration audit.'

    def handle(self, *args, **options):
        SiteSetting.objects.update_or_create(
            id=1,
            defaults={
                'site_name': 'Saber Tech Logistics',
                'tagline': 'Trusted Solutions, Every Mile',
                'footer_text': 'Saber Tech © 2026 • Built on ATMP-core • Owner and operator centric logistics platform.',
                'facebook_url': 'https://www.facebook.com/sabertechlogistics',
                'instagram_url': 'https://www.instagram.com/sabertechlogistics',
                'logo': 'site/logo.png',
                'favicon': 'site/favicon.png',
            },
        )

        page_by_slug = {}
        for page_data in PAGES:
            page, _ = Page.objects.update_or_create(
                slug=page_data['slug'],
                defaults={
                    'title': page_data['title'],
                    'nav_label': page_data.get('nav_label', ''),
                    'template': page_data['template'],
                    'eyebrow': page_data.get('eyebrow', ''),
                    'subtitle': page_data.get('subtitle', ''),
                    'body': page_data.get('body', ''),
                    'show_in_main_nav': page_data.get('show_in_main_nav', False),
                    'show_in_footer': page_data.get('show_in_footer', False),
                    'sort_order': page_data['sort_order'],
                    'is_published': True,
                },
            )
            page_by_slug[page.slug] = page

        ContentBlock.objects.all().delete()
        for slug, blocks in BLOCKS.items():
            page = page_by_slug[slug]
            for index, (heading, body, link_label, link_url) in enumerate(blocks):
                ContentBlock.objects.create(
                    page=page,
                    heading=heading,
                    body=f'<p>{body}</p>',
                    link_label=link_label,
                    link_url=link_url,
                    sort_order=index * 10,
                )

        NavigationLink.objects.all().delete()
        for page in Page.objects.filter(show_in_main_nav=True).order_by('sort_order'):
            NavigationLink.objects.create(
                label=page.nav_label or page.title,
                url=page.get_absolute_url(),
                location='header',
                sort_order=page.sort_order,
            )
        for page in Page.objects.filter(show_in_footer=True).exclude(slug__in={'privacy-policy', 'term-and-conditions'}).order_by('sort_order'):
            location = 'footer_support' if page.slug in {'about', 'privacy-policy', 'term-and-conditions'} else 'footer_quick'
            label = page.nav_label or page.title
            if page.slug == 'contact-us':
                label = 'Contact'
            NavigationLink.objects.create(
                label=label,
                url=page.get_absolute_url(),
                location=location,
                sort_order=page.sort_order,
            )
        for index, (label, url) in enumerate([
            ('Customer Order Portal', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/customer-pwa/'),
            ('Driver App', 'https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-pwa/'),
        ], start=200):
            NavigationLink.objects.create(
                label=label,
                url=url,
                location='footer_support',
                sort_order=index,
                open_in_new_tab=True,
            )

        TeamMember.objects.all().delete()
        for index, (name, title, email, phone, photo, is_featured) in enumerate(TEAM):
            TeamMember.objects.create(
                name=name,
                title=title,
                email=email,
                phone=phone,
                photo=photo,
                is_featured=is_featured,
                sort_order=index * 10,
                is_active=True,
            )

        self.stdout.write(self.style.SUCCESS('Seeded Saber Tech CMS content.'))
