from django.db.models import Prefetch
from django.core.cache import cache
from .models import SiteConfig, Company, FooterPage, FaqCategory, BlogCategory, BlogPost, Announcement

def site_config(request):
    # Try to get from cache first
    cached_context = cache.get('global_site_config_context')
    if cached_context:
        return cached_context

    try:
        config = SiteConfig.objects.first()
    except:
        config = None
        
    companies = list(Company.objects.filter(is_show_on_home=True).order_by('order'))
    top_pick_companies = list(Company.objects.filter(is_top_pick=True).order_by('order'))
    legal_pages = list(FooterPage.objects.filter(is_active=True, category='legal').order_by('order'))
    company_pages = list(FooterPage.objects.filter(is_active=True, category='companies').order_by('order'))
    faq_roots = list(FaqCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order'))
    announcements = list(Announcement.objects.filter(is_active=True).order_by('order'))
    faq_popular_roots = list(FaqCategory.objects.filter(is_active=True, parent__isnull=True, is_popular=True).order_by('order'))
    blog_roots = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order'))
    blog_nav_roots = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True).order_by('order'))
    
    posts_prefetch = Prefetch('posts', queryset=BlogPost.objects.filter(is_active=True).order_by('order', 'title'))
    children_prefetch = Prefetch('children', queryset=BlogCategory.objects.filter(is_active=True).prefetch_related(posts_prefetch))
    
    blog_footer_roots = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_footer=True).prefetch_related(children_prefetch).order_by('order'))

    blog_nav_quotes = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='quotes').prefetch_related(children_prefetch).order_by('order'))
    blog_nav_companies = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='companies').prefetch_related(children_prefetch).order_by('order'))
    blog_nav_cost = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='cost').prefetch_related(children_prefetch).order_by('order'))
    blog_nav_save = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='save').prefetch_related(children_prefetch).order_by('order'))
    blog_nav_resources = list(BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='resources').prefetch_related(children_prefetch).order_by('order'))
    
    # Get latest 4 posts from resources categories
    footer_resource_posts = list(BlogPost.objects.filter(category__nav_group='resources', is_active=True).order_by('-updated_at')[:4])

    context = {
        'site_config': config,
        'global_companies': companies,
        'top_pick_companies': top_pick_companies,
        'footer_legal_pages': legal_pages,
        'footer_company_pages': company_pages,
        'faq_root_categories': faq_roots,
        'faq_popular_root_categories': faq_popular_roots,
        'blog_root_categories': blog_roots,
        'blog_nav_root_categories': blog_nav_roots,
        'blog_footer_root_categories': blog_footer_roots,
        'blog_nav_quotes': blog_nav_quotes,
        'blog_nav_companies': blog_nav_companies,
        'blog_nav_cost': blog_nav_cost,
        'blog_nav_save': blog_nav_save,
        'blog_nav_resources': blog_nav_resources,
        'footer_resource_posts': footer_resource_posts,
        'announcements': announcements,
    }
    
    # Cache the context for 5 minutes (300 seconds)
    cache.set('global_site_config_context', context, 300)
    
    return context
