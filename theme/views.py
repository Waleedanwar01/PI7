from django.shortcuts import render
from core.models import Company, HomeVideo, QuickFAQ, BlogCategory, BlogPost
from django.db.models import Prefetch

def home(request):
    companies = Company.objects.filter(is_show_on_home=True).order_by('order')
    videos = HomeVideo.objects.filter(is_active=True).order_by('order')
    quick_faqs = QuickFAQ.objects.filter(is_active=True).order_by('order')
    
    # Fetch posts for specific home sections
    # Recommendations
    rec_posts = BlogPost.objects.filter(show_in_recommendations=True, is_active=True).order_by('order', 'id')[:3]
    if not rec_posts:
        rec_posts = BlogPost.objects.filter(category__name="Recommendations", is_active=True).order_by('id')[:3]
    
    # Guides
    guide_posts = BlogPost.objects.filter(show_in_guides=True, is_active=True).order_by('order', 'id')[:3]
    if not guide_posts:
        guide_posts = BlogPost.objects.filter(category__name="Guides", is_active=True).order_by('id')[:3]
    
    # Driving Research
    research_posts = BlogPost.objects.filter(show_in_research=True, is_active=True).order_by('order', 'id')[:3]
    if not research_posts:
        research_posts = BlogPost.objects.filter(category__name="Driving Research", is_active=True).order_by('id')[:3]

    # Popular Topics
    popular_posts = BlogPost.objects.filter(is_popular=True, is_active=True).order_by('order', 'id')[:6]

    # Fetch "Best" category children for "Our Top Recommendations"
    try:
        best_category = BlogCategory.objects.get(name="Best", is_active=True)
        # Prefetch posts to optimize first_post property access in template
        posts_prefetch = Prefetch('posts', queryset=BlogPost.objects.filter(is_active=True).order_by('order', 'title'))
        best_subcategories = best_category.children.filter(is_active=True).prefetch_related(posts_prefetch).order_by('id')
    except BlogCategory.DoesNotExist:
        best_subcategories = []
    
    return render(request, "home.html", {
        'companies': companies, 
        'videos': videos,
        'quick_faqs': quick_faqs,
        'rec_posts': rec_posts,
        'guide_posts': guide_posts,
        'research_posts': research_posts,
        'popular_posts': popular_posts,
        'best_subcategories': best_subcategories,
    })
