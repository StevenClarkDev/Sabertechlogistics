from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import select_template

from .models import ContactSubmission, NavigationLink, Page, SiteSetting, TeamMember


def site_context():
    settings = SiteSetting.objects.first()
    links = NavigationLink.objects.filter(is_active=True)
    return {
        'site_settings': settings,
        'header_links': links.filter(location='header'),
        'footer_quick_links': links.filter(location='footer_quick'),
        'footer_support_links': links.filter(location='footer_support'),
    }


def render_page(request, page):
    context = site_context()
    context['page'] = page
    context['blocks'] = page.blocks.filter(is_active=True)

    if page.template in {'home', 'leadership'}:
        context['featured_team'] = TeamMember.objects.filter(is_active=True, is_featured=True)
        context['team_members'] = TeamMember.objects.filter(is_active=True)

    template = select_template([
        f'cms/pages/{page.slug or "home"}.html',
        f'cms/{page.template}.html',
    ])
    return render(request, template.template.name, context)


def home(request):
    page = get_object_or_404(Page, slug='', is_published=True)
    return render_page(request, page)


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    if page.template == 'contact' and request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            name = ' '.join([
                request.POST.get('first_name', '').strip(),
                request.POST.get('last_name', '').strip(),
            ]).strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactSubmission.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been received.')
            return redirect(page.get_absolute_url())
        messages.error(request, 'Name, email, and message are required.')
    return render_page(request, page)
