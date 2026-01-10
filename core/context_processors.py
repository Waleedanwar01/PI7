from django.db.models import Prefetch
from .models import SiteConfig, Company, FooterPage, FaqCategory, BlogCategory, BlogPost, Announcement

def site_config(request):
    try:
        config = SiteConfig.objects.first()
    except:
        config = None
        
    companies = Company.objects.filter(is_show_on_home=True).order_by('order')
    top_pick_companies = Company.objects.filter(is_top_pick=True).order_by('order')
    legal_pages = FooterPage.objects.filter(is_active=True, category='legal').order_by('order')
    company_pages = FooterPage.objects.filter(is_active=True, category='companies').order_by('order')
    faq_roots = FaqCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    announcements = Announcement.objects.filter(is_active=True).order_by('order')
    faq_popular_roots = FaqCategory.objects.filter(is_active=True, parent__isnull=True, is_popular=True).order_by('order')
    blog_roots = BlogCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    blog_nav_roots = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True).order_by('order')
    
    posts_prefetch = Prefetch('posts', queryset=BlogPost.objects.filter(is_active=True).order_by('order', 'title'))
    children_prefetch = Prefetch('children', queryset=BlogCategory.objects.filter(is_active=True).prefetch_related(posts_prefetch))
    
    blog_footer_roots = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_footer=True).prefetch_related(children_prefetch).order_by('order')

    blog_nav_quotes = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='quotes').prefetch_related(children_prefetch).order_by('order')
    blog_nav_companies = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='companies').prefetch_related(children_prefetch).order_by('order')
    blog_nav_cost = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='cost').prefetch_related(children_prefetch).order_by('order')
    blog_nav_save = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='save').prefetch_related(children_prefetch).order_by('order')
    blog_nav_resources = BlogCategory.objects.filter(is_active=True, parent__isnull=True, show_in_navbar=True, nav_group='resources').prefetch_related(children_prefetch).order_by('order')
    
    # Get latest 4 posts from resources categories
    footer_resource_posts = BlogPost.objects.filter(category__nav_group='resources', is_active=True).order_by('-updated_at')[:4]

    return {
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
