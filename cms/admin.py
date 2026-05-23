from django.contrib import admin

from .models import (
    ContactSubmission,
    ContentBlock,
    NavigationLink,
    Page,
    SiteSetting,
    TeamMember,
)

admin.site.site_header = 'Saber Tech CMS'
admin.site.site_title = 'Saber Tech CMS'
admin.site.index_title = 'Website administration'


class ContentBlockInline(admin.StackedInline):
    model = ContentBlock
    extra = 0
    fields = (
        'sort_order',
        'is_active',
        'eyebrow',
        'heading',
        'body',
        'link_label',
        'link_url',
        'image',
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'template',
        'is_published',
        'show_in_main_nav',
        'show_in_footer',
        'sort_order',
        'updated_at',
    )
    list_editable = ('is_published', 'show_in_main_nav', 'show_in_footer', 'sort_order')
    list_filter = ('template', 'is_published', 'show_in_main_nav', 'show_in_footer')
    search_fields = ('title', 'slug', 'subtitle', 'body', 'seo_title', 'seo_description')
    inlines = [ContentBlockInline]
    fieldsets = (
        ('Page', {
            'fields': (
                'title',
                'slug',
                'nav_label',
                'template',
                'is_published',
                'show_in_main_nav',
                'show_in_footer',
                'sort_order',
            )
        }),
        ('Content', {'fields': ('eyebrow', 'subtitle', 'body')}),
        ('SEO basics', {
            'description': 'Control how this page appears in search engines.',
            'fields': (
                'seo_title',
                'seo_description',
                'seo_keywords',
                'canonical_url',
                'seo_noindex',
                'seo_nofollow',
            ),
        }),
        ('Social sharing', {
            'classes': ('collapse',),
            'description': 'Optional overrides for Facebook, LinkedIn, X/Twitter, and other previews.',
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
            'classes': ('collapse',),
            'fields': ('structured_data_json',),
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'email', 'updated_at')
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'tagline', 'footer_text', 'logo', 'favicon')}),
        ('Contact and Social', {'fields': ('phone', 'email', 'facebook_url', 'instagram_url')}),
        ('SEO defaults', {
            'description': 'Fallback metadata used when individual pages leave SEO fields blank.',
            'fields': (
                'site_url',
                'default_seo_title',
                'default_seo_description',
                'default_seo_keywords',
                'default_og_image',
            ),
        }),
        ('Third-party scripts and tracking', {
            'description': (
                'Paste Google tags, live chat widgets, pixels, verification tags, '
                'and other third-party embeds here. Code is rendered exactly as entered.'
            ),
            'fields': (
                'analytics_head_code',
                'analytics_body_code',
                'third_party_footer_code',
            ),
        }),
    )


@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'location', 'sort_order', 'open_in_new_tab', 'is_active')
    list_editable = ('sort_order', 'open_in_new_tab', 'is_active')
    list_filter = ('location', 'is_active', 'open_in_new_tab')
    search_fields = ('label', 'url')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'sort_order', 'is_featured', 'is_active')
    list_editable = ('sort_order', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('name', 'title', 'email')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_reviewed', 'created_at')
    list_editable = ('is_reviewed',)
    list_filter = ('is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at', 'updated_at')
