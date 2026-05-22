from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSetting(TimeStampedModel):
    site_name = models.CharField(max_length=120, default='Saber Tech Logistics')
    tagline = models.CharField(max_length=180, default='Trusted Solutions, Every Mile')
    footer_text = models.CharField(
        max_length=220,
        default='Saber Tech © 2026 • Built on ATMP-core • Owner and operator centric logistics platform.',
    )
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    analytics_head_code = models.TextField(
        blank=True,
        verbose_name='Head scripts',
        help_text='Paste scripts that must appear before </head>, such as Google Analytics, verification tags, pixels, or CSS snippets.',
    )
    analytics_body_code = models.TextField(
        blank=True,
        verbose_name='Opening body scripts',
        help_text='Paste scripts that must appear immediately after <body>, such as the Google Tag Manager noscript iframe.',
    )
    third_party_footer_code = models.TextField(
        blank=True,
        verbose_name='Before closing body scripts',
        help_text='Paste live chat widgets, tracking scripts, and other third-party code that should load near the end of the page.',
    )

    class Meta:
        verbose_name = 'Site setting'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.site_name


class Page(TimeStampedModel):
    TEMPLATE_CHOICES = [
        ('home', 'Home'),
        ('standard', 'Standard page'),
        ('leadership', 'Leadership'),
        ('contact', 'Contact'),
        ('legal', 'Legal'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        help_text='Leave blank only for the home page.',
    )
    nav_label = models.CharField(max_length=80, blank=True)
    subtitle = models.CharField(max_length=220, blank=True)
    eyebrow = models.CharField(max_length=80, blank=True)
    body = models.TextField(blank=True, help_text='Main page content. HTML is allowed.')
    template = models.CharField(max_length=30, choices=TEMPLATE_CHOICES, default='standard')
    seo_title = models.CharField(max_length=180, blank=True)
    seo_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    show_in_main_nav = models.BooleanField(default=False)
    show_in_footer = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if not self.slug:
            return reverse('cms:home')
        return reverse('cms:page_detail', kwargs={'slug': self.slug})


class ContentBlock(TimeStampedModel):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
    heading = models.CharField(max_length=180)
    eyebrow = models.CharField(max_length=80, blank=True)
    body = models.TextField(blank=True, help_text='Block content. HTML is allowed.')
    link_label = models.CharField(max_length=80, blank=True)
    link_url = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='blocks/', blank=True)
    sort_order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'heading']

    def __str__(self):
        return f'{self.page}: {self.heading}'


class NavigationLink(TimeStampedModel):
    LOCATION_CHOICES = [
        ('header', 'Header'),
        ('footer_quick', 'Footer quick links'),
        ('footer_support', 'Footer support'),
    ]

    label = models.CharField(max_length=80)
    url = models.CharField(max_length=300)
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES, default='header')
    sort_order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    open_in_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['location', 'sort_order', 'label']

    def __str__(self):
        return f'{self.get_location_display()}: {self.label}'


class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='team/', blank=True)
    sort_order = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class ContactSubmission(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}>'
