# Saber Tech Logistics WordPress to Django Migration Audit

Source checked: https://sabertechlogistics.com/
Audit date: 2026-05-22

## Goal

Replicate the public WordPress site in Django with matching routes, content, visual layout, assets, and outbound links. The target host is an IBM server.

## Current Site Stack

- CMS: WordPress
- Theme: Astra 4.12.3
- Page builder: Elementor 3.35.5 and Elementor Pro 3.35.1
- SEO: All in One SEO 4.9.4.1
- Other visible plugins/services: ElementsKit Lite, Google Language Translator, MonsterInsights, Facebook Pixel, Google Tag Manager
- Server header: nginx/1.31.0
- Public API: WordPress REST API is enabled at `/wp-json/`
- Sitemap: `/sitemap.xml` points to `/page-sitemap.xml`

## Public Routes To Rebuild

| Current URL | Django route | Notes |
| --- | --- | --- |
| `/` | `/` | Home page. Highest priority; includes hero, process steps, customer section, service grid, driver section, leadership preview, footer. |
| `/atmp-courier/` | `/atmp-courier/` | Driver guide and ATMP-Courier content. WordPress title metadata currently says `ATMP-Core`, but visible heading says `ATMP Courier`. |
| `/atmp-core/` | `/atmp-core/` | ATMP-core positioning page. |
| `/customer-order/` | `/customer-order/` | Customer portal landing page with external PWA link. |
| `/driver-access/` | `/driver-access/` | Driver portal landing page with external sign-up/sign-in links. |
| `/leadership/` | `/leadership/` | Executive team grid. |
| `/press/` | `/press/` | Press announcement and media contact. |
| `/contact-us/` | `/contact-us/` | Contact page. Existing form is static and does not submit server-side. |
| `/about/` | `/about/` | About page. |
| `/privacy-policy/` | `/privacy-policy/` | Legal content. Effective date: 1/29/26. |
| `/term-and-conditions/` | `/term-and-conditions/` | Legal content. Keep slug as-is for URL parity, despite typo. |
| `/sample-page/` | exclude or redirect | Default WordPress sample page, likely should not be recreated publicly. |

## Navigation

Primary nav:

- Home
- ATMP-Courier
- ATMP-Core
- Customer Order
- Driver Access
- Leadership
- Press
- Contact Us

Footer quick links:

- ATMP-Courier
- ATMP-Core
- Customer Order
- Driver Access
- Leadership
- Press
- Contact

Footer support links:

- About
- Customer Order Portal
- Driver App
- Privacy Policy
- Terms & Conditions

## Important External Links

- Customer PWA: `https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/customer-pwa/`
- Driver PWA: `https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-pwa/`
- Driver sign-up: `https://sabertech-php-api.24aupl12h4kp.us-south.codeengine.appdomain.cloud/driver-signup/`
- iOS Driver: `https://apps.apple.com/gb/app/sabertech-driver/id6759118586`
- iOS Customer: `https://apps.apple.com/gb/app/sabertech-customer/id6759689343`
- Android Driver: `https://play.google.com/store/apps/details?id=com.sabertech.driver`
- Android Customer: `https://play.google.com/store/apps/details?id=com.sabertech.customer&hl=ln`
- Facebook: `https://www.facebook.com/sabertechlogistics`
- Instagram: `https://www.instagram.com/sabertechlogistics`

## Local Reference Files Collected

Screenshots:

- `migration/screenshots/home-full.png`
- `migration/screenshots/home-mobile-full.png`
- `migration/screenshots/atmp-courier-full.png`
- `migration/screenshots/atmp-core-full.png`
- `migration/screenshots/customer-order-full.png`
- `migration/screenshots/driver-access-full.png`
- `migration/screenshots/leadership-full.png`
- `migration/screenshots/leadership-mobile-full.png`
- `migration/screenshots/press-full.png`
- `migration/screenshots/contact-full.png`
- `migration/screenshots/about-full.png`
- `migration/screenshots/privacy-policy-full.png`
- `migration/screenshots/terms-full.png`

Assets:

- `migration/assets/cropped-SaberTech-Logistics-logo-design-final-file-01-scaled-1.png`
- `migration/assets/cropped-SaberTech-Logistics-logo-design-final-file-01-scaled-2-192x192.png`
- `migration/assets/cropped-SaberTech-Logistics-logo-design-final-file-01-scaled-2-32x32.png`
- `migration/assets/ceo-1.jpg`
- `migration/assets/cpo-1.jpg`
- `migration/assets/cpro-1.jpg`
- `migration/assets/coo-1.jpg`
- `migration/assets/clo-1.jpg`
- `migration/assets/cvo-1.jpg`
- `migration/assets/cto-1.jpg`
- `migration/assets/cmo-1.jpg`
- `migration/assets/cco-1.jpg`

## Content Model Draft

Use a simple Django app with mostly static templates first. A CMS is not required for a 1:1 rebuild unless the team wants non-developers to edit content later.

Recommended structure:

- `pages`: static page views and templates
- `static/images`: migrated logo and leadership photos
- `static/css/site.css`: hand-authored CSS matching the Elementor/Astra output
- `templates/base.html`: shared header/footer/nav
- `templates/pages/*.html`: individual page content

## Design Notes

- Fonts requested by current site source: Jost, Inder, Roboto, Roboto Slab.
- Site uses Astra/Elementor spacing and large section blocks.
- Footer repeats across pages with logo, tagline, social links, quick links, support links, copyright, privacy, and terms.
- Home page has app download buttons, including iOS and Android driver/customer links.
- Translation widget appears site-wide via Google Language Translator.
- Contact form currently says it does not process submissions server-side. For Django, either preserve the static behavior for parity or implement a real form endpoint.

## Implementation Risks / Decisions

- Need decide whether to recreate Google Translator, analytics, Facebook Pixel, and Google Tag Manager in the Django version.
- Need decide whether legal pages should be copied exactly or reviewed before launch.
- Need decide whether `/sample-page/` should return 404, redirect to `/about/`, or be recreated only temporarily.
- Need preserve the misspelled `/term-and-conditions/` route for existing SEO links.
- If the IBM server will run behind nginx, collect final deployment details before setting Django `ALLOWED_HOSTS`, static files, SSL, and process manager config.
