from django.contrib import admin

from .models import (
    ContactSubmission,
    ContentBlock,
    NavigationLink,
    Page,
    SiteSetting,
    TeamMember,
)


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
    search_fields = ('title', 'slug', 'subtitle', 'body')
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
        ('SEO', {'fields': ('seo_title', 'seo_description')}),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'email', 'updated_at')
    fieldsets = (
        ('Brand', {'fields': ('site_name', 'tagline', 'footer_text', 'logo', 'favicon')}),
        ('Contact and Social', {'fields': ('phone', 'email', 'facebook_url', 'instagram_url')}),
        ('Tracking Code', {
            'classes': ('collapse',),
            'fields': ('analytics_head_code', 'analytics_body_code'),
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
