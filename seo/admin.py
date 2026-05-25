from django.contrib import admin

from .models import PageSEO, SiteSEO


@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'seo_title',
        'has_meta_description',
        'robots',
        'updated_at',
    )
    list_filter = ('template', 'seo_noindex', 'seo_nofollow', 'is_published')
    search_fields = (
        'title',
        'slug',
        'seo_title',
        'seo_description',
        'seo_keywords',
        'canonical_url',
    )
    readonly_fields = ('title', 'slug', 'template', 'live_path', 'updated_at')
    fieldsets = (
        ('Page reference', {
            'description': 'Content, layout, and navigation are managed from Pages. This screen is only for metadata.',
            'fields': ('title', 'slug', 'template', 'live_path', 'updated_at'),
        }),
        ('Search engine metadata', {
            'fields': (
                'seo_title',
                'seo_description',
                'seo_keywords',
                'canonical_url',
                'seo_noindex',
                'seo_nofollow',
            ),
        }),
        ('Social sharing metadata', {
            'fields': (
                'og_title',
                'og_description',
                'og_image',
                'twitter_title',
                'twitter_description',
                'twitter_image',
            ),
        }),
        ('Structured data', {
            'description': 'Paste JSON-LD only. The website wraps it in an application/ld+json script tag.',
            'fields': ('structured_data_json',),
        }),
    )

    @admin.display(description='Meta description')
    def has_meta_description(self, obj):
        return 'Set' if obj.seo_description else 'Missing'

    @admin.display(description='Robots')
    def robots(self, obj):
        directives = []
        directives.append('noindex' if obj.seo_noindex else 'index')
        directives.append('nofollow' if obj.seo_nofollow else 'follow')
        return ', '.join(directives)

    @admin.display(description='Live path')
    def live_path(self, obj):
        return obj.get_absolute_url()

    def has_add_permission(self, request):
        return False


@admin.register(SiteSEO)
class SiteSEOAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_url', 'default_seo_title', 'updated_at')
    search_fields = (
        'site_name',
        'site_url',
        'default_seo_title',
        'default_seo_description',
        'default_seo_keywords',
    )
    fieldsets = (
        ('Global search defaults', {
            'description': 'Fallback metadata used when an individual page leaves its SEO fields blank.',
            'fields': (
                'site_url',
                'default_seo_title',
                'default_seo_description',
                'default_seo_keywords',
            ),
        }),
        ('Global social sharing default', {
            'fields': ('default_og_image',),
        }),
        ('Tracking and verification scripts', {
            'description': (
                'SEO and analytics snippets that must be rendered globally, such as Google tags, '
                'Search Console verification, pixels, and live chat widgets.'
            ),
            'fields': (
                'analytics_head_code',
                'analytics_body_code',
                'third_party_footer_code',
            ),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSEO.objects.exists()
