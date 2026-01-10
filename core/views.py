from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import os, time
from .models import ContactSubmission, FooterPage, TeamMember, FaqCategory, FaqPost, BlogCategory, BlogPost, QuickFAQ, ZipCode, Company, ZipRange

def zip_search(request):
    zip_code = request.GET.get('zip', '').strip()
    companies = []
    
    if zip_code:
        # 1. Try exact match first (legacy support)
        try:
            zip_obj = ZipCode.objects.get(code=zip_code)
            companies = list(zip_obj.companies.filter(is_show_on_home=True).order_by('order'))
        except ZipCode.DoesNotExist:
            companies = []

        # 2. Check ranges and state-wide companies
        if zip_code.isdigit():
            zip_int = int(zip_code)
            # Find all ranges that contain this zip code
            ranges = ZipRange.objects.filter(start_zip__lte=zip_int, end_zip__gte=zip_int)
            
            for r in ranges:
                # A. Companies assigned to the specific range
                range_companies = r.companies.filter(is_show_on_home=True).order_by('order')
                for c in range_companies:
                    if c not in companies:
                        companies.append(c)
                
                # B. Companies assigned to the STATE of this range
                if r.state:
                    state_companies = Company.objects.filter(states__code=r.state, is_show_on_home=True).order_by('order')
                    for c in state_companies:
                        if c not in companies:
                            companies.append(c)
            
            # Re-sort final list by order
            companies.sort(key=lambda x: x.order)
            
    return render(request, "zip_results.html", {'zip_code': zip_code, 'companies': companies})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactSubmission.objects.create(name=name, email=email, message=message)
            return render(request, "contact.html", {'success': True})
        return render(request, "contact.html", {'error': "Please fill all fields."})
    return render(request, "contact.html")

def footer_page(request, slug):
    link = f"/pages/{slug}/"
    page = get_object_or_404(FooterPage, link=link, is_active=True)
    team_members = None
    if slug == "about-us":
        team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    return render(request, "footer_page.html", {'page': page, 'team_members': team_members})

def team_member_detail(request, pk):
    member = get_object_or_404(TeamMember, pk=pk, is_active=True)
    return render(request, "team_member_detail.html", {'member': member})

def faq_home(request):
    categories = FaqCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    latest = FaqPost.objects.filter(is_active=True).order_by('-updated_at').first()
    return render(request, "faq_home.html", {
        'categories': categories,
        'last_updated': latest.updated_at if latest else None,
        'latest_post': latest
    })

def faq_category(request, slug):
    cat = get_object_or_404(FaqCategory, slug=slug, is_active=True)
    subcats = cat.children.filter(is_active=True).order_by('order')
    posts = cat.posts.filter(is_active=True).order_by('order')
    return render(request, "faq_category.html", {'category': cat, 'subcategories': subcats, 'posts': posts})

def faq_post_detail(request, slug):
    post = get_object_or_404(FaqPost, slug=slug, is_active=True)
    related = FaqPost.objects.filter(is_active=True, category=post.category).exclude(pk=post.pk).order_by('order')[:9]
    images = list(post.images.filter(is_active=True).order_by('order'))
    return render(request, "faq_post_detail.html", {'post': post, 'related_posts': related, 'images': images})

def companies_faqs(request):
    categories = FaqCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    latest = FaqPost.objects.filter(is_active=True).order_by('-updated_at').first()
    return render(request, "companies_faqs.html", {
        'categories': categories,
        'last_updated': latest.updated_at if latest else None,
        'latest_post': latest
    })

def blog_home(request):
    categories = BlogCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    latest = BlogPost.objects.filter(is_active=True).order_by('-updated_at').first()
    return render(request, "blog_home.html", {
        'categories': categories,
        'last_updated': latest.updated_at if latest else None,
    })

def blog_category(request, slug):
    cat = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    subcats = cat.children.filter(is_active=True).order_by('order')
    posts = cat.posts.filter(is_active=True).order_by('order')
    return render(request, "blog_category.html", {'category': cat, 'subcategories': subcats, 'posts': posts})

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_active=True)
    related = BlogPost.objects.filter(is_active=True, category=post.category).exclude(pk=post.pk).order_by('-updated_at')[:5]
    next_post = BlogPost.objects.filter(is_active=True, updated_at__lt=post.updated_at).order_by('-updated_at').first()
    return render(request, "blog_post_detail.html", {'post': post, 'related_posts': related, 'next_post': next_post})

@staff_member_required
@require_POST
def upload_editor_image(request):
    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    name, ext = os.path.splitext(f.name)
    ts = int(time.time())
    safe_name = f"{name[:40]}_{ts}{ext}"
    path = os.path.join('blog', 'editor', safe_name)
    saved = default_storage.save(path, f)
    url = default_storage.url(saved)
    return JsonResponse({'location': url})

def blog_list(request):
    posts_list = BlogPost.objects.filter(is_active=True).order_by('-updated_at')
    categories = BlogCategory.objects.filter(is_active=True, parent__isnull=True).order_by('order')
    
    paginator = Paginator(posts_list, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "blog_list.html", {
        'page_obj': page_obj,
        'categories': categories
    })

def search(request):
    query = request.GET.get('q', '').strip()
    blog_results = []
    faq_results = []
    
    if query:
        blog_results = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(summary__icontains=query),
            is_active=True
        ).distinct()
        
        faq_results = FaqPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query),
            is_active=True
        ).distinct()
        
    return render(request, "search_results.html", {
        'query': query,
        'blog_results': blog_results,
        'faq_results': faq_results
    })
