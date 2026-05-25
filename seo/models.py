from cms.models import Page, SiteSetting


class PageSEO(Page):
    class Meta:
        proxy = True
        verbose_name = 'Page SEO'
        verbose_name_plural = 'Page SEO'


class SiteSEO(SiteSetting):
    class Meta:
        proxy = True
        verbose_name = 'Main SEO setting'
        verbose_name_plural = 'Main SEO settings'
