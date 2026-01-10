"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from theme.views import home
from core.views import contact, footer_page, team_member_detail, faq_home, faq_category, faq_post_detail, companies_faqs, blog_home, blog_category, blog_post_detail, upload_editor_image, blog_list, search, zip_search
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('unlock-savings/', zip_search, name='zip_search'),
    path('contact/', contact, name='contact'),
    path('pages/<slug:slug>/', footer_page, name='footer_page'),
    path('team/<int:pk>/', team_member_detail, name='team_member_detail'),
    path('faq/', faq_home, name='faq_home'),
    path('faq/category/<slug:slug>/', faq_category, name='faq_category'),
    path('faq/post/<slug:slug>/', faq_post_detail, name='faq_post_detail'),
    path('companies/faqs/', companies_faqs, name='companies_faqs'),
    path('blog/', blog_home, name='blog_home'),
    path('blog/category/<slug:slug>/', blog_category, name='blog_category'),
    path('blog/post/<slug:slug>/', blog_post_detail, name='blog_post_detail'),
    path('blogs/', blog_list, name='blog_list'),
    path('search/', search, name='search'),
    path('zip-search/', zip_search, name='zip_search'),
    path('editor/upload/', upload_editor_image, name='editor_upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
