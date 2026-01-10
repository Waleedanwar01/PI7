from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import SiteConfig, Company, FooterPage, ContactSubmission, TeamMember, FaqCategory, FaqPost, FaqImage, HomeVideo, BlogCategory, BlogPost, BlogImage, QuickFAQ, Announcement, ZipCode, ZipRange, State

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(ZipRange)
class ZipRangeAdmin(admin.ModelAdmin):
    list_display = ('get_range_display', 'get_company_count')
    search_fields = ('start_zip', 'end_zip', 'state')
    list_filter = ('state',)
    filter_horizontal = ('companies',)
    
    def get_range_display(self, obj):
        return str(obj)
    get_range_display.short_description = 'Range / State'

    def get_company_count(self, obj):
        return obj.companies.count()
    get_company_count.short_description = 'Companies'

from django import forms

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'domain', 'order', 'is_show_on_home', 'is_top_pick')
    list_editable = ('rating', 'order', 'is_show_on_home', 'is_top_pick')
    search_fields = ('name', 'domain')
    filter_horizontal = ('states',)

@admin.register(FooterPage)
class FooterPageAdmin(admin.ModelAdmin):
    class FooterPageForm(forms.ModelForm):
        class Meta:
            model = FooterPage
            fields = '__all__'
            widgets = {
                'content': forms.Textarea(attrs={'class': 'tinymce', 'rows': 20}),
                'meta_description': forms.Textarea(attrs={'rows': 4}),
            }
        class Media:
            js = (
                'https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js',
                'js/footerpage.js',
            )
    form = FooterPageForm
    list_display = ('title', 'category', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'link', 'meta_title', 'meta_keywords')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'link', 'category', 'order', 'layout', 'is_active')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Editor me Pro Tip aur Note buttons ka istemal karein. Images ke liye Insert Image button, file picker ya paste (Ctrl+V) use karein.'
        }),
        ('SEO / Meta', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    class AnnouncementInline(admin.TabularInline):
        model = Announcement
        extra = 1
        fields = ('text', 'link', 'order', 'is_active')
    
    inlines = [AnnouncementInline]
    list_display = ('site_name', 'phone_number', 'email')
    fieldsets = (
        ('General Info', {
            'fields': ('site_name', 'phone_number', 'email', 'home_title', 'footer_text', 'address', 'footer_disclaimer', 'announcement_text')
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_button_text')
        }),
        ('Contact & Social', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url', 'youtube_channel_name')
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding more than one object
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        # Redirect to the edit page of the first object if it exists
        if self.model.objects.exists():
            obj = self.model.objects.first()
            return redirect(reverse('admin:core_siteconfig_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text', 'link')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    class TeamMemberForm(forms.ModelForm):
        class Meta:
            model = TeamMember
            fields = '__all__'
            widgets = {
                'description': forms.Textarea(attrs={'class': 'tinymce', 'rows': 16}),
            }
        class Media:
            js = (
                'https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js',
                'js/footerpage.js',
            )
    form = TeamMemberForm
    list_display = ('name', 'position', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'position')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'position', 'photo', 'order', 'is_active')
        }),
        ('About', {
            'fields': ('description',)
        }),
        ('Social Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url', 'website_url')
        }),
    )

@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active', 'is_popular')
    list_editable = ('order', 'is_active', 'is_popular')
    list_filter = ('is_active', 'parent', 'is_popular')
    search_fields = ('name', 'slug')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'parent', 'order', 'is_active', 'is_popular')
        }),
    )

@admin.register(FaqPost)
class FaqPostAdmin(admin.ModelAdmin):
    class ImageInline(admin.TabularInline):
        model = FaqImage
        extra = 1
        fields = ('image', 'caption', 'order', 'is_active')
    inlines = [ImageInline]
    class FaqPostForm(forms.ModelForm):
        class Meta:
            model = FaqPost
            fields = '__all__'
            widgets = {
                'content': forms.Textarea(attrs={'class': 'tinymce', 'rows': 20}),
                'meta_description': forms.Textarea(attrs={'rows': 4}),
                'summary': forms.Textarea(attrs={'rows': 4}),
            }
        class Media:
            js = (
                'https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js',
                'js/footerpage.js',
            )
    form = FaqPostForm
    list_display = ('title', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'slug', 'meta_title', 'meta_keywords')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'category', 'order', 'is_active')
        }),
        ('Summary', {
            'fields': ('summary',)
        }),
        ('Author', {
            'fields': (
                'author_name', 'author_photo', 'author_bio',
                'author_facebook_url', 'author_twitter_url',
                'author_instagram_url', 'author_linkedin_url',
                'author_website_url'
            )
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Editor me Pro Tip aur Note buttons ka istemal karein, ya shortcodes [protip]...[/protip] aur [note]...[/note] dal kar beautiful cards banayein.'
        }),
        ('SEO / Meta', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Images', {
            'fields': (),
            'description': 'Use the inline section below to manage gallery images. They will appear inside content and in the sidebar gallery.'
        }),
    )

@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'published_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'youtube_url')
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'youtube_url', 'order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('published_at',),
        }),
    )

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order', 'is_active', 'is_dropdown', 'show_in_navbar', 'show_in_footer', 'nav_group')
    list_editable = ('order', 'is_active', 'is_dropdown', 'show_in_navbar', 'show_in_footer', 'nav_group')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'slug')
    fieldsets = (
        ('Basic', {
            'fields': ('name', 'parent', 'order', 'is_active')
        }),
        ('Navigation', {
            'fields': ('is_dropdown', 'show_in_navbar', 'show_in_footer', 'nav_group'),
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    class ImageInline(admin.TabularInline):
        model = BlogImage
        extra = 1
        fields = ('image', 'caption', 'order', 'is_active')
    class BlogPostForm(forms.ModelForm):
        class CategoryChoiceField(forms.ModelChoiceField):
            def label_from_instance(self, obj):
                try:
                    if getattr(obj, 'company', None) and obj.name.lower().endswith(' general'):
                        return obj.company.name
                except Exception:
                    pass
                return obj.name
        class Meta:
            model = BlogPost
            fields = '__all__'
            widgets = {
                'content': forms.Textarea(attrs={'class': 'tinymce', 'rows': 20}),
                'meta_description': forms.Textarea(attrs={'rows': 4}),
                'summary': forms.Textarea(attrs={'rows': 4}),
            }
        class Media:
            js = (
                'https://cdn.jsdelivr.net/npm/tinymce@7.6.1/tinymce.min.js',
                'js/footerpage.js',
            )
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            from .models import Company
            # Ensure each company has at least one selectable category
            for c in Company.objects.order_by('name'):
                default_name = f"{c.name} General"
                exists = BlogCategory.objects.filter(name=default_name).exists()
                if not exists:
                    try:
                        bc = BlogCategory(name=default_name, company=c, is_active=True, order=0)
                        bc.save()
                    except Exception:
                        pass
            qs = BlogCategory.objects.filter(is_active=True).order_by('order', 'name')
            groups = {c.name: [] for c in Company.objects.order_by('name')}
            for obj in qs:
                group_label = obj.company.name if getattr(obj, 'company', None) else "Other Categories"
                groups.setdefault(group_label, []).append((obj.pk, obj.name))
            grouped_choices = [(k, v) for k, v in sorted(groups.items(), key=lambda x: x[0].lower())]
            field = self.CategoryChoiceField(queryset=qs, widget=self.fields['category'].widget, required=True)
            field.choices = grouped_choices
            field.widget.choices = grouped_choices
            field.help_text = "Categories grouped by company."
            self.fields['category'] = field
    form = BlogPostForm
    inlines = [ImageInline]
    list_display = ('title', 'category', 'order', 'is_active', 'is_popular', 'show_in_recommendations', 'show_in_guides', 'show_in_research')
    list_editable = ('order', 'is_active', 'is_popular', 'show_in_recommendations', 'show_in_guides', 'show_in_research')
    list_filter = ('category', 'is_active', 'is_popular', 'show_in_recommendations', 'show_in_guides', 'show_in_research')
    search_fields = ('title', 'slug', 'meta_title', 'meta_keywords')
    exclude = ('companies',)
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'category', 'order', 'is_active')
        }),
        ('Homepage Visibility', {
            'fields': ('is_popular', 'show_in_recommendations', 'show_in_guides', 'show_in_research'),
            'description': 'Select where this post should appear on the homepage.'
        }),
        ('Summary', {
            'fields': ('summary',)
        }),
        ('Media', {
            'fields': ('hero_image', 'icon')
        }),
        ('Author', {
            'fields': ('author_name', 'author_photo', 'author_bio')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('SEO / Meta', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        co = getattr(obj.category, 'company', None)
        if co:
            obj.companies.set([co])
        else:
            obj.companies.clear()

@admin.register(QuickFAQ)
class QuickFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('question', 'answer')
